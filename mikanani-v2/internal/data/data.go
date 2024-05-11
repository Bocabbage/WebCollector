package data

import (
	"context"
	"mikanani-v2/internal/conf"
	"mikanani-v2/internal/data/ent"
	"time"

	_ "github.com/go-sql-driver/mysql"

	"ariga.io/entcache"
	dialectSql "entgo.io/ent/dialect/sql"
	"github.com/go-kratos/kratos/v2/log"
	rdsv8 "github.com/go-redis/redis/v8"
	"github.com/google/wire"
	"github.com/redis/go-redis/v9"
	"go.mongodb.org/mongo-driver/mongo"
	mongoOpt "go.mongodb.org/mongo-driver/mongo/options"
)

// ProviderSet is data providers.
var ProviderSet = wire.NewSet(NewData, NewAnimeDocRepo, NewAnimeMetaRepo, NewAnimeStateRepo)

// Data .
type Data struct {
	mysqlDb  *ent.Client   // mysql
	redisCli *redis.Client // redis
	mongoCli *mongo.Client // mongo
}

// NewData .
func NewData(c *conf.Data, logger log.Logger) (*Data, func(), error) {
	log := log.NewHelper(logger)
	// ------ Mysql Client init ------
	sqlDrv, err := dialectSql.Open(
		c.Database.Driver,
		c.Database.Source,
	)

	if err != nil {
		log.Errorf("[NewData]failed at sql.Open: %v, source: %v", err, c.Database.Source)
		return nil, nil, err
	}

	sqlDrvCache := entcache.NewDriver(
		sqlDrv,
		entcache.TTL(1*time.Hour),
		entcache.Levels(
			entcache.NewLRU(256),
			entcache.NewRedis(rdsv8.NewClient(
				&rdsv8.Options{
					Addr:     c.Redis.Addr,
					Password: c.Redis.Password,
					DB:       int(c.Redis.Db),
				},
			)),
		),
	)

	mysqlClient := ent.NewClient(ent.Driver(sqlDrvCache))

	// ----- Redis Client init -----
	cfg := redis.Options{
		Addr:     c.Redis.Addr,
		Password: c.Redis.Password,
		DB:       int(c.Redis.Db),
	}
	redisClient := redis.NewClient(&cfg)
	rdsCtx, rdsCancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer rdsCancel()
	if err := redisClient.Ping(rdsCtx).Err(); err != nil {
		log.Error("[NewData]redis ping take too much time, regarded as failed.")
		return nil, nil, err
	}

	// ----- Mongo Client init -----
	mongoOpt := mongoOpt.Client().ApplyURI(c.Mongo.Host)
	mongoClient, err := mongo.Connect(context.Background(), mongoOpt)
	if err != nil {
		log.Error("[Newdata]failed at mongo.Connect(): %v", err)
		return nil, nil, err
	}
	mongoCtx, mongoCancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer mongoCancel()
	if err := mongoClient.Ping(mongoCtx, nil); err != nil {
		log.Error("[NewData]mongo ping take too much time, regarded as failed.")
		return nil, nil, err
	}

	d := &Data{
		mysqlDb:  mysqlClient,
		redisCli: redisClient,
		mongoCli: mongoClient,
	}

	cleanup := func() {
		log.Info("closing the data resources")
		// Mysql clean up
		if err := d.mysqlDb.Close(); err != nil {
			log.Errorf("[DataCleanup]close d.mysqldb error: %v", err)
		}
		// Redis clean up
		if err := d.redisCli.Close(); err != nil {
			log.Errorf("[DataCleanup]close d.redisCli error: %v", err)
		}
		// Mongo clean up
		if err := d.mongoCli.Disconnect(context.Background()); err != nil {
			log.Errorf("[DataCleanup]close d.mongoCli error: %v", err)
		}
		log.Info("finish closing the data resources")
	}
	return d, cleanup, nil
}
