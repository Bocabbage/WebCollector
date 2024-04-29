package data

import (
	"context"
	"mikanani-v2/internal/biz"
	"mikanani-v2/internal/conf"

	"github.com/go-kratos/kratos/v2/log"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type animeDocRepo struct {
	data       *Data
	log        *log.Helper
	database   string
	collection string
}

func NewAnimeDocRepo(data *Data, conf *conf.Data, logger log.Logger) biz.AnimeDocRepo {
	return &animeDocRepo{
		data:       data,
		log:        log.NewHelper(logger),
		database:   conf.Mongo.Mikandb,
		collection: conf.Mongo.Mikancollection,
	}
}

func (adrp *animeDocRepo) QueryByUid(ctx context.Context, uid int64) (*biz.AnimeDoc, error) {
	coll := adrp.data.mongoCli.Database(adrp.database).Collection(adrp.collection)

	var result biz.AnimeDoc
	filter := bson.M{"uid": uid}
	projection := bson.M{"_id": 0}
	err := coll.FindOne(ctx, filter, options.FindOne().SetProjection(projection)).Decode(&result)
	if err != nil {
		return nil, err
	}
	return &result, nil
}

func (adrp *animeDocRepo) Insert(ctx context.Context, doc *biz.AnimeDoc) error {
	coll := adrp.data.mongoCli.Database(adrp.database).Collection(adrp.collection)
	_, err := coll.InsertOne(ctx, doc)
	if err == nil {
		adrp.log.Infof("[animeDocRepo.Insert][uid-%d]success.", doc.Uid)
	}
	return err
}

func (adrp *animeDocRepo) Update(ctx context.Context, doc *biz.AnimeDoc) error {
	coll := adrp.data.mongoCli.Database(adrp.database).Collection(adrp.collection)
	filter := bson.M{"uid": doc.Uid}
	update := bson.M{"$set": doc}
	opts := options.Update().SetUpsert(true)

	_, err := coll.UpdateOne(ctx, filter, update, opts)
	if err == nil {
		adrp.log.Infof("[animeDocRepo.Update][uid-%d]success.", doc.Uid)
	}
	return err
}

func (adrp *animeDocRepo) Delete(ctx context.Context, uid int64) error {
	coll := adrp.data.mongoCli.Database(adrp.database).Collection(adrp.collection)
	filter := bson.M{"uid": uid}

	_, err := coll.DeleteOne(ctx, filter)
	if err == nil {
		adrp.log.Infof("[animeDocRepo.Delete][uid-%d]success.", uid)
	}
	return err
}
