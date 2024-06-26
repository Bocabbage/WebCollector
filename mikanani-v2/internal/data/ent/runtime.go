// Code generated by ent, DO NOT EDIT.

package ent

import (
	"mikanani-v2/internal/data/ent/animemeta"
	"mikanani-v2/internal/data/ent/schema"
	"time"
)

// The init function reads all schema descriptors with runtime code
// (default values, validators, hooks and policies) and stitches it
// to their package variables.
func init() {
	animemetaFields := schema.AnimeMeta{}.Fields()
	_ = animemetaFields
	// animemetaDescName is the schema descriptor for name field.
	animemetaDescName := animemetaFields[1].Descriptor()
	// animemeta.NameValidator is a validator for the "name" field. It is called by the builders before save.
	animemeta.NameValidator = func() func(string) error {
		validators := animemetaDescName.Validators
		fns := [...]func(string) error{
			validators[0].(func(string) error),
			validators[1].(func(string) error),
		}
		return func(name string) error {
			for _, fn := range fns {
				if err := fn(name); err != nil {
					return err
				}
			}
			return nil
		}
	}()
	// animemetaDescDownloadBitmap is the schema descriptor for downloadBitmap field.
	animemetaDescDownloadBitmap := animemetaFields[2].Descriptor()
	// animemeta.DefaultDownloadBitmap holds the default value on creation for the downloadBitmap field.
	animemeta.DefaultDownloadBitmap = animemetaDescDownloadBitmap.Default.(int64)
	// animemetaDescIsActive is the schema descriptor for isActive field.
	animemetaDescIsActive := animemetaFields[3].Descriptor()
	// animemeta.DefaultIsActive holds the default value on creation for the isActive field.
	animemeta.DefaultIsActive = animemetaDescIsActive.Default.(bool)
	// animemetaDescEpisodes is the schema descriptor for episodes field.
	animemetaDescEpisodes := animemetaFields[5].Descriptor()
	// animemeta.DefaultEpisodes holds the default value on creation for the episodes field.
	animemeta.DefaultEpisodes = animemetaDescEpisodes.Default.(int64)
	// animemeta.EpisodesValidator is a validator for the "episodes" field. It is called by the builders before save.
	animemeta.EpisodesValidator = animemetaDescEpisodes.Validators[0].(func(int64) error)
	// animemetaDescCreateTime is the schema descriptor for createTime field.
	animemetaDescCreateTime := animemetaFields[6].Descriptor()
	// animemeta.DefaultCreateTime holds the default value on creation for the createTime field.
	animemeta.DefaultCreateTime = animemetaDescCreateTime.Default.(func() time.Time)
	// animemetaDescUpdateTime is the schema descriptor for updateTime field.
	animemetaDescUpdateTime := animemetaFields[7].Descriptor()
	// animemeta.DefaultUpdateTime holds the default value on creation for the updateTime field.
	animemeta.DefaultUpdateTime = animemetaDescUpdateTime.Default.(func() time.Time)
}
