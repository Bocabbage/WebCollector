package schema

import (
	"time"

	"entgo.io/ent"
	"entgo.io/ent/dialect"
	"entgo.io/ent/schema/field"
)

// ArticleMeta holds the schema definition for the ArticleMeta entity.
type ArticleMeta struct {
	ent.Schema
}

// Fields of the ArticleMeta.
func (ArticleMeta) Fields() []ent.Field {
	return []ent.Field{
		field.Int64("uid").Unique(),
		field.String("title").NotEmpty(),
		field.JSON("tags", []string{}),
		field.Time("createTime").Default(time.Now).SchemaType(map[string]string{
			dialect.MySQL: "datetime",
		}),
		field.Time("updateTime").Default(time.Now).SchemaType(map[string]string{
			dialect.MySQL: "datetime",
		}),
	}
}

// Edges of the ArticleMeta.
func (ArticleMeta) Edges() []ent.Edge {
	return nil
}
