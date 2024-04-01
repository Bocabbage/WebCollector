package data

import (
	"context"
	"fmt"
	"news-subscriber-bff/internal/conf"
	"news-subscriber-bff/internal/data/ent"

	"entgo.io/ent/dialect"
	dialectSql "entgo.io/ent/dialect/sql"
	"github.com/go-kratos/kratos/v2/log"
	"github.com/google/wire"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/trace"
)

// ProviderSet is data providers.
var ProviderSet = wire.NewSet(NewData, NewArticleRepo)

// Data .
type Data struct {
	db *ent.Client // mysql
}

// NewData .
func NewData(c *conf.Data, logger log.Logger) (*Data, func(), error) {
	log := log.NewHelper(logger)
	drv, err := dialectSql.Open(
		c.Database.Driver,
		c.Database.Source,
	)

	if err != nil {
		log.Errorf("failed at sql.Open: %v", err)
		return nil, nil, err
	}

	sqlDrv := dialect.DebugWithContext(drv, func(ctx context.Context, i ...interface{}) {
		log.Info(i...)
		tracer := otel.Tracer("ent.")
		kind := trace.SpanKindServer
		_, span := tracer.Start(
			ctx,
			"Query",
			trace.WithAttributes(
				attribute.String("sql", fmt.Sprint(i...)),
			),
			trace.WithSpanKind(kind),
		)
		span.End()
	})
	// Get MySQL client
	client := ent.NewClient(ent.Driver(sqlDrv))
	d := &Data{db: client}

	cleanup := func() {
		log.Info("closing the data resources")
		if err := d.db.Close(); err != nil {
			log.Error("close d.db error: %v", err)
		}
	}
	return d, cleanup, nil
}
