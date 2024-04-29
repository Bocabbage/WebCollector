package schema

import (
	"time"

	"entgo.io/ent"
	"entgo.io/ent/dialect"
	"entgo.io/ent/schema/field"
)

// AnimeMeta holds the schema definition for the AnimeMeta entity.
type AnimeMeta struct {
	ent.Schema
}

// Fields of the AnimeMeta.
func (AnimeMeta) Fields() []ent.Field {
	return []ent.Field{
		// field.Int64("id") default defined in Ent
		field.Int64("uid").Unique(),
		field.String("name").Unique().NotEmpty().MaxLen(128),
		field.Int64("downloadBitmap").Default(0),
		field.Bool("isActive").Default(false),
		field.JSON("tags", []string{}).Optional(),
		field.Int64("episodes").Default(24).Immutable().Max(52),
		field.Time("createTime").Default(time.Now).SchemaType(map[string]string{
			dialect.MySQL: "datetime",
		}),
		field.Time("updateTime").Default(time.Now).SchemaType(map[string]string{
			dialect.MySQL: "datetime",
		}),
	}
}

// Edges of the AnimeMeta.
func (AnimeMeta) Edges() []ent.Edge {
	return nil
}
