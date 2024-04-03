// Code generated by protoc-gen-validate. DO NOT EDIT.
// source: newssub/v1/article.proto

package v1

import (
	"bytes"
	"errors"
	"fmt"
	"net"
	"net/mail"
	"net/url"
	"regexp"
	"sort"
	"strings"
	"time"
	"unicode/utf8"

	"google.golang.org/protobuf/types/known/anypb"
)

// ensure the imports are used
var (
	_ = bytes.MinRead
	_ = errors.New("")
	_ = fmt.Print
	_ = utf8.UTFMax
	_ = (*regexp.Regexp)(nil)
	_ = (*strings.Reader)(nil)
	_ = net.IPv4len
	_ = time.Duration(0)
	_ = (*url.URL)(nil)
	_ = (*mail.Address)(nil)
	_ = anypb.Any{}
	_ = sort.Sort
)

// Validate checks the field values on ArticleItem with the rules defined in
// the proto definition for this message. If any rules are violated, the first
// error encountered is returned, or nil if there are no violations.
func (m *ArticleItem) Validate() error {
	return m.validate(false)
}

// ValidateAll checks the field values on ArticleItem with the rules defined in
// the proto definition for this message. If any rules are violated, the
// result is a list of violation errors wrapped in ArticleItemMultiError, or
// nil if none found.
func (m *ArticleItem) ValidateAll() error {
	return m.validate(true)
}

func (m *ArticleItem) validate(all bool) error {
	if m == nil {
		return nil
	}

	var errors []error

	// no validation rules for Uid

	// no validation rules for Title

	// no validation rules for Content

	if len(errors) > 0 {
		return ArticleItemMultiError(errors)
	}

	return nil
}

// ArticleItemMultiError is an error wrapping multiple validation errors
// returned by ArticleItem.ValidateAll() if the designated constraints aren't met.
type ArticleItemMultiError []error

// Error returns a concatenation of all the error messages it wraps.
func (m ArticleItemMultiError) Error() string {
	var msgs []string
	for _, err := range m {
		msgs = append(msgs, err.Error())
	}
	return strings.Join(msgs, "; ")
}

// AllErrors returns a list of validation violation errors.
func (m ArticleItemMultiError) AllErrors() []error { return m }

// ArticleItemValidationError is the validation error returned by
// ArticleItem.Validate if the designated constraints aren't met.
type ArticleItemValidationError struct {
	field  string
	reason string
	cause  error
	key    bool
}

// Field function returns field value.
func (e ArticleItemValidationError) Field() string { return e.field }

// Reason function returns reason value.
func (e ArticleItemValidationError) Reason() string { return e.reason }

// Cause function returns cause value.
func (e ArticleItemValidationError) Cause() error { return e.cause }

// Key function returns key value.
func (e ArticleItemValidationError) Key() bool { return e.key }

// ErrorName returns error name.
func (e ArticleItemValidationError) ErrorName() string { return "ArticleItemValidationError" }

// Error satisfies the builtin error interface
func (e ArticleItemValidationError) Error() string {
	cause := ""
	if e.cause != nil {
		cause = fmt.Sprintf(" | caused by: %v", e.cause)
	}

	key := ""
	if e.key {
		key = "key for "
	}

	return fmt.Sprintf(
		"invalid %sArticleItem.%s: %s%s",
		key,
		e.field,
		e.reason,
		cause)
}

var _ error = ArticleItemValidationError{}

var _ interface {
	Field() string
	Reason() string
	Key() bool
	Cause() error
	ErrorName() string
} = ArticleItemValidationError{}

// Validate checks the field values on CreateArticleRequest with the rules
// defined in the proto definition for this message. If any rules are
// violated, the first error encountered is returned, or nil if there are no violations.
func (m *CreateArticleRequest) Validate() error {
	return m.validate(false)
}

// ValidateAll checks the field values on CreateArticleRequest with the rules
// defined in the proto definition for this message. If any rules are
// violated, the result is a list of violation errors wrapped in
// CreateArticleRequestMultiError, or nil if none found.
func (m *CreateArticleRequest) ValidateAll() error {
	return m.validate(true)
}

func (m *CreateArticleRequest) validate(all bool) error {
	if m == nil {
		return nil
	}

	var errors []error

	if l := utf8.RuneCountInString(m.GetTitle()); l < 5 || l > 50 {
		err := CreateArticleRequestValidationError{
			field:  "Title",
			reason: "value length must be between 5 and 50 runes, inclusive",
		}
		if !all {
			return err
		}
		errors = append(errors, err)
	}

	// no validation rules for Content

	if len(errors) > 0 {
		return CreateArticleRequestMultiError(errors)
	}

	return nil
}

// CreateArticleRequestMultiError is an error wrapping multiple validation
// errors returned by CreateArticleRequest.ValidateAll() if the designated
// constraints aren't met.
type CreateArticleRequestMultiError []error

// Error returns a concatenation of all the error messages it wraps.
func (m CreateArticleRequestMultiError) Error() string {
	var msgs []string
	for _, err := range m {
		msgs = append(msgs, err.Error())
	}
	return strings.Join(msgs, "; ")
}

// AllErrors returns a list of validation violation errors.
func (m CreateArticleRequestMultiError) AllErrors() []error { return m }

// CreateArticleRequestValidationError is the validation error returned by
// CreateArticleRequest.Validate if the designated constraints aren't met.
type CreateArticleRequestValidationError struct {
	field  string
	reason string
	cause  error
	key    bool
}

// Field function returns field value.
func (e CreateArticleRequestValidationError) Field() string { return e.field }

// Reason function returns reason value.
func (e CreateArticleRequestValidationError) Reason() string { return e.reason }

// Cause function returns cause value.
func (e CreateArticleRequestValidationError) Cause() error { return e.cause }

// Key function returns key value.
func (e CreateArticleRequestValidationError) Key() bool { return e.key }

// ErrorName returns error name.
func (e CreateArticleRequestValidationError) ErrorName() string {
	return "CreateArticleRequestValidationError"
}

// Error satisfies the builtin error interface
func (e CreateArticleRequestValidationError) Error() string {
	cause := ""
	if e.cause != nil {
		cause = fmt.Sprintf(" | caused by: %v", e.cause)
	}

	key := ""
	if e.key {
		key = "key for "
	}

	return fmt.Sprintf(
		"invalid %sCreateArticleRequest.%s: %s%s",
		key,
		e.field,
		e.reason,
		cause)
}

var _ error = CreateArticleRequestValidationError{}

var _ interface {
	Field() string
	Reason() string
	Key() bool
	Cause() error
	ErrorName() string
} = CreateArticleRequestValidationError{}

// Validate checks the field values on CreateArticleReply with the rules
// defined in the proto definition for this message. If any rules are
// violated, the first error encountered is returned, or nil if there are no violations.
func (m *CreateArticleReply) Validate() error {
	return m.validate(false)
}

// ValidateAll checks the field values on CreateArticleReply with the rules
// defined in the proto definition for this message. If any rules are
// violated, the result is a list of violation errors wrapped in
// CreateArticleReplyMultiError, or nil if none found.
func (m *CreateArticleReply) ValidateAll() error {
	return m.validate(true)
}

func (m *CreateArticleReply) validate(all bool) error {
	if m == nil {
		return nil
	}

	var errors []error

	// no validation rules for Uid

	if len(errors) > 0 {
		return CreateArticleReplyMultiError(errors)
	}

	return nil
}

// CreateArticleReplyMultiError is an error wrapping multiple validation errors
// returned by CreateArticleReply.ValidateAll() if the designated constraints
// aren't met.
type CreateArticleReplyMultiError []error

// Error returns a concatenation of all the error messages it wraps.
func (m CreateArticleReplyMultiError) Error() string {
	var msgs []string
	for _, err := range m {
		msgs = append(msgs, err.Error())
	}
	return strings.Join(msgs, "; ")
}

// AllErrors returns a list of validation violation errors.
func (m CreateArticleReplyMultiError) AllErrors() []error { return m }

// CreateArticleReplyValidationError is the validation error returned by
// CreateArticleReply.Validate if the designated constraints aren't met.
type CreateArticleReplyValidationError struct {
	field  string
	reason string
	cause  error
	key    bool
}

// Field function returns field value.
func (e CreateArticleReplyValidationError) Field() string { return e.field }

// Reason function returns reason value.
func (e CreateArticleReplyValidationError) Reason() string { return e.reason }

// Cause function returns cause value.
func (e CreateArticleReplyValidationError) Cause() error { return e.cause }

// Key function returns key value.
func (e CreateArticleReplyValidationError) Key() bool { return e.key }

// ErrorName returns error name.
func (e CreateArticleReplyValidationError) ErrorName() string {
	return "CreateArticleReplyValidationError"
}

// Error satisfies the builtin error interface
func (e CreateArticleReplyValidationError) Error() string {
	cause := ""
	if e.cause != nil {
		cause = fmt.Sprintf(" | caused by: %v", e.cause)
	}

	key := ""
	if e.key {
		key = "key for "
	}

	return fmt.Sprintf(
		"invalid %sCreateArticleReply.%s: %s%s",
		key,
		e.field,
		e.reason,
		cause)
}

var _ error = CreateArticleReplyValidationError{}

var _ interface {
	Field() string
	Reason() string
	Key() bool
	Cause() error
	ErrorName() string
} = CreateArticleReplyValidationError{}

// Validate checks the field values on UpdateArticleRequest with the rules
// defined in the proto definition for this message. If any rules are
// violated, the first error encountered is returned, or nil if there are no violations.
func (m *UpdateArticleRequest) Validate() error {
	return m.validate(false)
}

// ValidateAll checks the field values on UpdateArticleRequest with the rules
// defined in the proto definition for this message. If any rules are
// violated, the result is a list of violation errors wrapped in
// UpdateArticleRequestMultiError, or nil if none found.
func (m *UpdateArticleRequest) ValidateAll() error {
	return m.validate(true)
}

func (m *UpdateArticleRequest) validate(all bool) error {
	if m == nil {
		return nil
	}

	var errors []error

	// no validation rules for Uid

	// no validation rules for Title

	// no validation rules for Content

	if len(errors) > 0 {
		return UpdateArticleRequestMultiError(errors)
	}

	return nil
}

// UpdateArticleRequestMultiError is an error wrapping multiple validation
// errors returned by UpdateArticleRequest.ValidateAll() if the designated
// constraints aren't met.
type UpdateArticleRequestMultiError []error

// Error returns a concatenation of all the error messages it wraps.
func (m UpdateArticleRequestMultiError) Error() string {
	var msgs []string
	for _, err := range m {
		msgs = append(msgs, err.Error())
	}
	return strings.Join(msgs, "; ")
}

// AllErrors returns a list of validation violation errors.
func (m UpdateArticleRequestMultiError) AllErrors() []error { return m }

// UpdateArticleRequestValidationError is the validation error returned by
// UpdateArticleRequest.Validate if the designated constraints aren't met.
type UpdateArticleRequestValidationError struct {
	field  string
	reason string
	cause  error
	key    bool
}

// Field function returns field value.
func (e UpdateArticleRequestValidationError) Field() string { return e.field }

// Reason function returns reason value.
func (e UpdateArticleRequestValidationError) Reason() string { return e.reason }

// Cause function returns cause value.
func (e UpdateArticleRequestValidationError) Cause() error { return e.cause }

// Key function returns key value.
func (e UpdateArticleRequestValidationError) Key() bool { return e.key }

// ErrorName returns error name.
func (e UpdateArticleRequestValidationError) ErrorName() string {
	return "UpdateArticleRequestValidationError"
}

// Error satisfies the builtin error interface
func (e UpdateArticleRequestValidationError) Error() string {
	cause := ""
	if e.cause != nil {
		cause = fmt.Sprintf(" | caused by: %v", e.cause)
	}

	key := ""
	if e.key {
		key = "key for "
	}

	return fmt.Sprintf(
		"invalid %sUpdateArticleRequest.%s: %s%s",
		key,
		e.field,
		e.reason,
		cause)
}

var _ error = UpdateArticleRequestValidationError{}

var _ interface {
	Field() string
	Reason() string
	Key() bool
	Cause() error
	ErrorName() string
} = UpdateArticleRequestValidationError{}

// Validate checks the field values on UpdateArticleReply with the rules
// defined in the proto definition for this message. If any rules are
// violated, the first error encountered is returned, or nil if there are no violations.
func (m *UpdateArticleReply) Validate() error {
	return m.validate(false)
}

// ValidateAll checks the field values on UpdateArticleReply with the rules
// defined in the proto definition for this message. If any rules are
// violated, the result is a list of violation errors wrapped in
// UpdateArticleReplyMultiError, or nil if none found.
func (m *UpdateArticleReply) ValidateAll() error {
	return m.validate(true)
}

func (m *UpdateArticleReply) validate(all bool) error {
	if m == nil {
		return nil
	}

	var errors []error

	if len(errors) > 0 {
		return UpdateArticleReplyMultiError(errors)
	}

	return nil
}

// UpdateArticleReplyMultiError is an error wrapping multiple validation errors
// returned by UpdateArticleReply.ValidateAll() if the designated constraints
// aren't met.
type UpdateArticleReplyMultiError []error

// Error returns a concatenation of all the error messages it wraps.
func (m UpdateArticleReplyMultiError) Error() string {
	var msgs []string
	for _, err := range m {
		msgs = append(msgs, err.Error())
	}
	return strings.Join(msgs, "; ")
}

// AllErrors returns a list of validation violation errors.
func (m UpdateArticleReplyMultiError) AllErrors() []error { return m }

// UpdateArticleReplyValidationError is the validation error returned by
// UpdateArticleReply.Validate if the designated constraints aren't met.
type UpdateArticleReplyValidationError struct {
	field  string
	reason string
	cause  error
	key    bool
}

// Field function returns field value.
func (e UpdateArticleReplyValidationError) Field() string { return e.field }

// Reason function returns reason value.
func (e UpdateArticleReplyValidationError) Reason() string { return e.reason }

// Cause function returns cause value.
func (e UpdateArticleReplyValidationError) Cause() error { return e.cause }

// Key function returns key value.
func (e UpdateArticleReplyValidationError) Key() bool { return e.key }

// ErrorName returns error name.
func (e UpdateArticleReplyValidationError) ErrorName() string {
	return "UpdateArticleReplyValidationError"
}

// Error satisfies the builtin error interface
func (e UpdateArticleReplyValidationError) Error() string {
	cause := ""
	if e.cause != nil {
		cause = fmt.Sprintf(" | caused by: %v", e.cause)
	}

	key := ""
	if e.key {
		key = "key for "
	}

	return fmt.Sprintf(
		"invalid %sUpdateArticleReply.%s: %s%s",
		key,
		e.field,
		e.reason,
		cause)
}

var _ error = UpdateArticleReplyValidationError{}

var _ interface {
	Field() string
	Reason() string
	Key() bool
	Cause() error
	ErrorName() string
} = UpdateArticleReplyValidationError{}

// Validate checks the field values on DeleteArticleRequest with the rules
// defined in the proto definition for this message. If any rules are
// violated, the first error encountered is returned, or nil if there are no violations.
func (m *DeleteArticleRequest) Validate() error {
	return m.validate(false)
}

// ValidateAll checks the field values on DeleteArticleRequest with the rules
// defined in the proto definition for this message. If any rules are
// violated, the result is a list of violation errors wrapped in
// DeleteArticleRequestMultiError, or nil if none found.
func (m *DeleteArticleRequest) ValidateAll() error {
	return m.validate(true)
}

func (m *DeleteArticleRequest) validate(all bool) error {
	if m == nil {
		return nil
	}

	var errors []error

	// no validation rules for Uid

	if len(errors) > 0 {
		return DeleteArticleRequestMultiError(errors)
	}

	return nil
}

// DeleteArticleRequestMultiError is an error wrapping multiple validation
// errors returned by DeleteArticleRequest.ValidateAll() if the designated
// constraints aren't met.
type DeleteArticleRequestMultiError []error

// Error returns a concatenation of all the error messages it wraps.
func (m DeleteArticleRequestMultiError) Error() string {
	var msgs []string
	for _, err := range m {
		msgs = append(msgs, err.Error())
	}
	return strings.Join(msgs, "; ")
}

// AllErrors returns a list of validation violation errors.
func (m DeleteArticleRequestMultiError) AllErrors() []error { return m }

// DeleteArticleRequestValidationError is the validation error returned by
// DeleteArticleRequest.Validate if the designated constraints aren't met.
type DeleteArticleRequestValidationError struct {
	field  string
	reason string
	cause  error
	key    bool
}

// Field function returns field value.
func (e DeleteArticleRequestValidationError) Field() string { return e.field }

// Reason function returns reason value.
func (e DeleteArticleRequestValidationError) Reason() string { return e.reason }

// Cause function returns cause value.
func (e DeleteArticleRequestValidationError) Cause() error { return e.cause }

// Key function returns key value.
func (e DeleteArticleRequestValidationError) Key() bool { return e.key }

// ErrorName returns error name.
func (e DeleteArticleRequestValidationError) ErrorName() string {
	return "DeleteArticleRequestValidationError"
}

// Error satisfies the builtin error interface
func (e DeleteArticleRequestValidationError) Error() string {
	cause := ""
	if e.cause != nil {
		cause = fmt.Sprintf(" | caused by: %v", e.cause)
	}

	key := ""
	if e.key {
		key = "key for "
	}

	return fmt.Sprintf(
		"invalid %sDeleteArticleRequest.%s: %s%s",
		key,
		e.field,
		e.reason,
		cause)
}

var _ error = DeleteArticleRequestValidationError{}

var _ interface {
	Field() string
	Reason() string
	Key() bool
	Cause() error
	ErrorName() string
} = DeleteArticleRequestValidationError{}

// Validate checks the field values on DeleteArticleReply with the rules
// defined in the proto definition for this message. If any rules are
// violated, the first error encountered is returned, or nil if there are no violations.
func (m *DeleteArticleReply) Validate() error {
	return m.validate(false)
}

// ValidateAll checks the field values on DeleteArticleReply with the rules
// defined in the proto definition for this message. If any rules are
// violated, the result is a list of violation errors wrapped in
// DeleteArticleReplyMultiError, or nil if none found.
func (m *DeleteArticleReply) ValidateAll() error {
	return m.validate(true)
}

func (m *DeleteArticleReply) validate(all bool) error {
	if m == nil {
		return nil
	}

	var errors []error

	if len(errors) > 0 {
		return DeleteArticleReplyMultiError(errors)
	}

	return nil
}

// DeleteArticleReplyMultiError is an error wrapping multiple validation errors
// returned by DeleteArticleReply.ValidateAll() if the designated constraints
// aren't met.
type DeleteArticleReplyMultiError []error

// Error returns a concatenation of all the error messages it wraps.
func (m DeleteArticleReplyMultiError) Error() string {
	var msgs []string
	for _, err := range m {
		msgs = append(msgs, err.Error())
	}
	return strings.Join(msgs, "; ")
}

// AllErrors returns a list of validation violation errors.
func (m DeleteArticleReplyMultiError) AllErrors() []error { return m }

// DeleteArticleReplyValidationError is the validation error returned by
// DeleteArticleReply.Validate if the designated constraints aren't met.
type DeleteArticleReplyValidationError struct {
	field  string
	reason string
	cause  error
	key    bool
}

// Field function returns field value.
func (e DeleteArticleReplyValidationError) Field() string { return e.field }

// Reason function returns reason value.
func (e DeleteArticleReplyValidationError) Reason() string { return e.reason }

// Cause function returns cause value.
func (e DeleteArticleReplyValidationError) Cause() error { return e.cause }

// Key function returns key value.
func (e DeleteArticleReplyValidationError) Key() bool { return e.key }

// ErrorName returns error name.
func (e DeleteArticleReplyValidationError) ErrorName() string {
	return "DeleteArticleReplyValidationError"
}

// Error satisfies the builtin error interface
func (e DeleteArticleReplyValidationError) Error() string {
	cause := ""
	if e.cause != nil {
		cause = fmt.Sprintf(" | caused by: %v", e.cause)
	}

	key := ""
	if e.key {
		key = "key for "
	}

	return fmt.Sprintf(
		"invalid %sDeleteArticleReply.%s: %s%s",
		key,
		e.field,
		e.reason,
		cause)
}

var _ error = DeleteArticleReplyValidationError{}

var _ interface {
	Field() string
	Reason() string
	Key() bool
	Cause() error
	ErrorName() string
} = DeleteArticleReplyValidationError{}

// Validate checks the field values on GetArticleRequest with the rules defined
// in the proto definition for this message. If any rules are violated, the
// first error encountered is returned, or nil if there are no violations.
func (m *GetArticleRequest) Validate() error {
	return m.validate(false)
}

// ValidateAll checks the field values on GetArticleRequest with the rules
// defined in the proto definition for this message. If any rules are
// violated, the result is a list of violation errors wrapped in
// GetArticleRequestMultiError, or nil if none found.
func (m *GetArticleRequest) ValidateAll() error {
	return m.validate(true)
}

func (m *GetArticleRequest) validate(all bool) error {
	if m == nil {
		return nil
	}

	var errors []error

	// no validation rules for Uid

	if len(errors) > 0 {
		return GetArticleRequestMultiError(errors)
	}

	return nil
}

// GetArticleRequestMultiError is an error wrapping multiple validation errors
// returned by GetArticleRequest.ValidateAll() if the designated constraints
// aren't met.
type GetArticleRequestMultiError []error

// Error returns a concatenation of all the error messages it wraps.
func (m GetArticleRequestMultiError) Error() string {
	var msgs []string
	for _, err := range m {
		msgs = append(msgs, err.Error())
	}
	return strings.Join(msgs, "; ")
}

// AllErrors returns a list of validation violation errors.
func (m GetArticleRequestMultiError) AllErrors() []error { return m }

// GetArticleRequestValidationError is the validation error returned by
// GetArticleRequest.Validate if the designated constraints aren't met.
type GetArticleRequestValidationError struct {
	field  string
	reason string
	cause  error
	key    bool
}

// Field function returns field value.
func (e GetArticleRequestValidationError) Field() string { return e.field }

// Reason function returns reason value.
func (e GetArticleRequestValidationError) Reason() string { return e.reason }

// Cause function returns cause value.
func (e GetArticleRequestValidationError) Cause() error { return e.cause }

// Key function returns key value.
func (e GetArticleRequestValidationError) Key() bool { return e.key }

// ErrorName returns error name.
func (e GetArticleRequestValidationError) ErrorName() string {
	return "GetArticleRequestValidationError"
}

// Error satisfies the builtin error interface
func (e GetArticleRequestValidationError) Error() string {
	cause := ""
	if e.cause != nil {
		cause = fmt.Sprintf(" | caused by: %v", e.cause)
	}

	key := ""
	if e.key {
		key = "key for "
	}

	return fmt.Sprintf(
		"invalid %sGetArticleRequest.%s: %s%s",
		key,
		e.field,
		e.reason,
		cause)
}

var _ error = GetArticleRequestValidationError{}

var _ interface {
	Field() string
	Reason() string
	Key() bool
	Cause() error
	ErrorName() string
} = GetArticleRequestValidationError{}

// Validate checks the field values on GetArticleReply with the rules defined
// in the proto definition for this message. If any rules are violated, the
// first error encountered is returned, or nil if there are no violations.
func (m *GetArticleReply) Validate() error {
	return m.validate(false)
}

// ValidateAll checks the field values on GetArticleReply with the rules
// defined in the proto definition for this message. If any rules are
// violated, the result is a list of violation errors wrapped in
// GetArticleReplyMultiError, or nil if none found.
func (m *GetArticleReply) ValidateAll() error {
	return m.validate(true)
}

func (m *GetArticleReply) validate(all bool) error {
	if m == nil {
		return nil
	}

	var errors []error

	if all {
		switch v := interface{}(m.GetArticle()).(type) {
		case interface{ ValidateAll() error }:
			if err := v.ValidateAll(); err != nil {
				errors = append(errors, GetArticleReplyValidationError{
					field:  "Article",
					reason: "embedded message failed validation",
					cause:  err,
				})
			}
		case interface{ Validate() error }:
			if err := v.Validate(); err != nil {
				errors = append(errors, GetArticleReplyValidationError{
					field:  "Article",
					reason: "embedded message failed validation",
					cause:  err,
				})
			}
		}
	} else if v, ok := interface{}(m.GetArticle()).(interface{ Validate() error }); ok {
		if err := v.Validate(); err != nil {
			return GetArticleReplyValidationError{
				field:  "Article",
				reason: "embedded message failed validation",
				cause:  err,
			}
		}
	}

	if len(errors) > 0 {
		return GetArticleReplyMultiError(errors)
	}

	return nil
}

// GetArticleReplyMultiError is an error wrapping multiple validation errors
// returned by GetArticleReply.ValidateAll() if the designated constraints
// aren't met.
type GetArticleReplyMultiError []error

// Error returns a concatenation of all the error messages it wraps.
func (m GetArticleReplyMultiError) Error() string {
	var msgs []string
	for _, err := range m {
		msgs = append(msgs, err.Error())
	}
	return strings.Join(msgs, "; ")
}

// AllErrors returns a list of validation violation errors.
func (m GetArticleReplyMultiError) AllErrors() []error { return m }

// GetArticleReplyValidationError is the validation error returned by
// GetArticleReply.Validate if the designated constraints aren't met.
type GetArticleReplyValidationError struct {
	field  string
	reason string
	cause  error
	key    bool
}

// Field function returns field value.
func (e GetArticleReplyValidationError) Field() string { return e.field }

// Reason function returns reason value.
func (e GetArticleReplyValidationError) Reason() string { return e.reason }

// Cause function returns cause value.
func (e GetArticleReplyValidationError) Cause() error { return e.cause }

// Key function returns key value.
func (e GetArticleReplyValidationError) Key() bool { return e.key }

// ErrorName returns error name.
func (e GetArticleReplyValidationError) ErrorName() string { return "GetArticleReplyValidationError" }

// Error satisfies the builtin error interface
func (e GetArticleReplyValidationError) Error() string {
	cause := ""
	if e.cause != nil {
		cause = fmt.Sprintf(" | caused by: %v", e.cause)
	}

	key := ""
	if e.key {
		key = "key for "
	}

	return fmt.Sprintf(
		"invalid %sGetArticleReply.%s: %s%s",
		key,
		e.field,
		e.reason,
		cause)
}

var _ error = GetArticleReplyValidationError{}

var _ interface {
	Field() string
	Reason() string
	Key() bool
	Cause() error
	ErrorName() string
} = GetArticleReplyValidationError{}

// Validate checks the field values on ListArticleRequest with the rules
// defined in the proto definition for this message. If any rules are
// violated, the first error encountered is returned, or nil if there are no violations.
func (m *ListArticleRequest) Validate() error {
	return m.validate(false)
}

// ValidateAll checks the field values on ListArticleRequest with the rules
// defined in the proto definition for this message. If any rules are
// violated, the result is a list of violation errors wrapped in
// ListArticleRequestMultiError, or nil if none found.
func (m *ListArticleRequest) ValidateAll() error {
	return m.validate(true)
}

func (m *ListArticleRequest) validate(all bool) error {
	if m == nil {
		return nil
	}

	var errors []error

	// no validation rules for Start

	// no validation rules for End

	if len(errors) > 0 {
		return ListArticleRequestMultiError(errors)
	}

	return nil
}

// ListArticleRequestMultiError is an error wrapping multiple validation errors
// returned by ListArticleRequest.ValidateAll() if the designated constraints
// aren't met.
type ListArticleRequestMultiError []error

// Error returns a concatenation of all the error messages it wraps.
func (m ListArticleRequestMultiError) Error() string {
	var msgs []string
	for _, err := range m {
		msgs = append(msgs, err.Error())
	}
	return strings.Join(msgs, "; ")
}

// AllErrors returns a list of validation violation errors.
func (m ListArticleRequestMultiError) AllErrors() []error { return m }

// ListArticleRequestValidationError is the validation error returned by
// ListArticleRequest.Validate if the designated constraints aren't met.
type ListArticleRequestValidationError struct {
	field  string
	reason string
	cause  error
	key    bool
}

// Field function returns field value.
func (e ListArticleRequestValidationError) Field() string { return e.field }

// Reason function returns reason value.
func (e ListArticleRequestValidationError) Reason() string { return e.reason }

// Cause function returns cause value.
func (e ListArticleRequestValidationError) Cause() error { return e.cause }

// Key function returns key value.
func (e ListArticleRequestValidationError) Key() bool { return e.key }

// ErrorName returns error name.
func (e ListArticleRequestValidationError) ErrorName() string {
	return "ListArticleRequestValidationError"
}

// Error satisfies the builtin error interface
func (e ListArticleRequestValidationError) Error() string {
	cause := ""
	if e.cause != nil {
		cause = fmt.Sprintf(" | caused by: %v", e.cause)
	}

	key := ""
	if e.key {
		key = "key for "
	}

	return fmt.Sprintf(
		"invalid %sListArticleRequest.%s: %s%s",
		key,
		e.field,
		e.reason,
		cause)
}

var _ error = ListArticleRequestValidationError{}

var _ interface {
	Field() string
	Reason() string
	Key() bool
	Cause() error
	ErrorName() string
} = ListArticleRequestValidationError{}

// Validate checks the field values on ListArticleReply with the rules defined
// in the proto definition for this message. If any rules are violated, the
// first error encountered is returned, or nil if there are no violations.
func (m *ListArticleReply) Validate() error {
	return m.validate(false)
}

// ValidateAll checks the field values on ListArticleReply with the rules
// defined in the proto definition for this message. If any rules are
// violated, the result is a list of violation errors wrapped in
// ListArticleReplyMultiError, or nil if none found.
func (m *ListArticleReply) ValidateAll() error {
	return m.validate(true)
}

func (m *ListArticleReply) validate(all bool) error {
	if m == nil {
		return nil
	}

	var errors []error

	for idx, item := range m.GetArticles() {
		_, _ = idx, item

		if all {
			switch v := interface{}(item).(type) {
			case interface{ ValidateAll() error }:
				if err := v.ValidateAll(); err != nil {
					errors = append(errors, ListArticleReplyValidationError{
						field:  fmt.Sprintf("Articles[%v]", idx),
						reason: "embedded message failed validation",
						cause:  err,
					})
				}
			case interface{ Validate() error }:
				if err := v.Validate(); err != nil {
					errors = append(errors, ListArticleReplyValidationError{
						field:  fmt.Sprintf("Articles[%v]", idx),
						reason: "embedded message failed validation",
						cause:  err,
					})
				}
			}
		} else if v, ok := interface{}(item).(interface{ Validate() error }); ok {
			if err := v.Validate(); err != nil {
				return ListArticleReplyValidationError{
					field:  fmt.Sprintf("Articles[%v]", idx),
					reason: "embedded message failed validation",
					cause:  err,
				}
			}
		}

	}

	if len(errors) > 0 {
		return ListArticleReplyMultiError(errors)
	}

	return nil
}

// ListArticleReplyMultiError is an error wrapping multiple validation errors
// returned by ListArticleReply.ValidateAll() if the designated constraints
// aren't met.
type ListArticleReplyMultiError []error

// Error returns a concatenation of all the error messages it wraps.
func (m ListArticleReplyMultiError) Error() string {
	var msgs []string
	for _, err := range m {
		msgs = append(msgs, err.Error())
	}
	return strings.Join(msgs, "; ")
}

// AllErrors returns a list of validation violation errors.
func (m ListArticleReplyMultiError) AllErrors() []error { return m }

// ListArticleReplyValidationError is the validation error returned by
// ListArticleReply.Validate if the designated constraints aren't met.
type ListArticleReplyValidationError struct {
	field  string
	reason string
	cause  error
	key    bool
}

// Field function returns field value.
func (e ListArticleReplyValidationError) Field() string { return e.field }

// Reason function returns reason value.
func (e ListArticleReplyValidationError) Reason() string { return e.reason }

// Cause function returns cause value.
func (e ListArticleReplyValidationError) Cause() error { return e.cause }

// Key function returns key value.
func (e ListArticleReplyValidationError) Key() bool { return e.key }

// ErrorName returns error name.
func (e ListArticleReplyValidationError) ErrorName() string { return "ListArticleReplyValidationError" }

// Error satisfies the builtin error interface
func (e ListArticleReplyValidationError) Error() string {
	cause := ""
	if e.cause != nil {
		cause = fmt.Sprintf(" | caused by: %v", e.cause)
	}

	key := ""
	if e.key {
		key = "key for "
	}

	return fmt.Sprintf(
		"invalid %sListArticleReply.%s: %s%s",
		key,
		e.field,
		e.reason,
		cause)
}

var _ error = ListArticleReplyValidationError{}

var _ interface {
	Field() string
	Reason() string
	Key() bool
	Cause() error
	ErrorName() string
} = ListArticleReplyValidationError{}
