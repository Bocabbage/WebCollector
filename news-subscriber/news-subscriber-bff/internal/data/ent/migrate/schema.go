// Code generated by ent, DO NOT EDIT.

package migrate

import (
	"entgo.io/ent/dialect/sql/schema"
	"entgo.io/ent/schema/field"
)

var (
	// ArticleMetaColumns holds the columns for the "article_meta" table.
	ArticleMetaColumns = []*schema.Column{
		{Name: "id", Type: field.TypeInt, Increment: true},
		{Name: "uid", Type: field.TypeInt64, Unique: true},
		{Name: "title", Type: field.TypeString},
		{Name: "tags", Type: field.TypeJSON},
		{Name: "create_time", Type: field.TypeTime, SchemaType: map[string]string{"mysql": "datetime"}},
		{Name: "update_time", Type: field.TypeTime, SchemaType: map[string]string{"mysql": "datetime"}},
	}
	// ArticleMetaTable holds the schema information for the "article_meta" table.
	ArticleMetaTable = &schema.Table{
		Name:       "article_meta",
		Columns:    ArticleMetaColumns,
		PrimaryKey: []*schema.Column{ArticleMetaColumns[0]},
	}
	// Tables holds all the tables in the schema.
	Tables = []*schema.Table{
		ArticleMetaTable,
	}
)

func init() {
}
