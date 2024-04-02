// Code generated by protoc-gen-go-http. DO NOT EDIT.
// versions:
// - protoc-gen-go-http v2.7.3
// - protoc             v3.20.3
// source: api/newssub/v1/article.proto

package v1

import (
	context "context"
	http "github.com/go-kratos/kratos/v2/transport/http"
	binding "github.com/go-kratos/kratos/v2/transport/http/binding"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the kratos package it is being compiled against.
var _ = new(context.Context)
var _ = binding.EncodeURL

const _ = http.SupportPackageIsVersion1

const OperationArticleCreateArticle = "/api.newssub.v1.Article/CreateArticle"
const OperationArticleDeleteArticle = "/api.newssub.v1.Article/DeleteArticle"
const OperationArticleGetArticle = "/api.newssub.v1.Article/GetArticle"
const OperationArticleListArticle = "/api.newssub.v1.Article/ListArticle"
const OperationArticleUpdateArticle = "/api.newssub.v1.Article/UpdateArticle"

type ArticleHTTPServer interface {
	CreateArticle(context.Context, *CreateArticleRequest) (*CreateArticleReply, error)
	DeleteArticle(context.Context, *DeleteArticleRequest) (*DeleteArticleReply, error)
	GetArticle(context.Context, *GetArticleRequest) (*GetArticleReply, error)
	ListArticle(context.Context, *ListArticleRequest) (*ListArticleReply, error)
	UpdateArticle(context.Context, *UpdateArticleRequest) (*UpdateArticleReply, error)
}

func RegisterArticleHTTPServer(s *http.Server, srv ArticleHTTPServer) {
	r := s.Route("/")
	r.POST("/newssub/v1/article/create", _Article_CreateArticle0_HTTP_Handler(srv))
	r.PUT("/newssub/v1/article/{uid}", _Article_UpdateArticle0_HTTP_Handler(srv))
	r.DELETE("/newssub/v1/article/{uid}", _Article_DeleteArticle0_HTTP_Handler(srv))
	r.GET("/newssub/v1/article/{uid}", _Article_GetArticle0_HTTP_Handler(srv))
	r.GET("/newssub/v1/article/list", _Article_ListArticle0_HTTP_Handler(srv))
}

func _Article_CreateArticle0_HTTP_Handler(srv ArticleHTTPServer) func(ctx http.Context) error {
	return func(ctx http.Context) error {
		var in CreateArticleRequest
		if err := ctx.Bind(&in); err != nil {
			return err
		}
		if err := ctx.BindQuery(&in); err != nil {
			return err
		}
		http.SetOperation(ctx, OperationArticleCreateArticle)
		h := ctx.Middleware(func(ctx context.Context, req interface{}) (interface{}, error) {
			return srv.CreateArticle(ctx, req.(*CreateArticleRequest))
		})
		out, err := h(ctx, &in)
		if err != nil {
			return err
		}
		reply := out.(*CreateArticleReply)
		return ctx.Result(200, reply)
	}
}

func _Article_UpdateArticle0_HTTP_Handler(srv ArticleHTTPServer) func(ctx http.Context) error {
	return func(ctx http.Context) error {
		var in UpdateArticleRequest
		if err := ctx.Bind(&in); err != nil {
			return err
		}
		if err := ctx.BindQuery(&in); err != nil {
			return err
		}
		if err := ctx.BindVars(&in); err != nil {
			return err
		}
		http.SetOperation(ctx, OperationArticleUpdateArticle)
		h := ctx.Middleware(func(ctx context.Context, req interface{}) (interface{}, error) {
			return srv.UpdateArticle(ctx, req.(*UpdateArticleRequest))
		})
		out, err := h(ctx, &in)
		if err != nil {
			return err
		}
		reply := out.(*UpdateArticleReply)
		return ctx.Result(200, reply)
	}
}

func _Article_DeleteArticle0_HTTP_Handler(srv ArticleHTTPServer) func(ctx http.Context) error {
	return func(ctx http.Context) error {
		var in DeleteArticleRequest
		if err := ctx.BindQuery(&in); err != nil {
			return err
		}
		if err := ctx.BindVars(&in); err != nil {
			return err
		}
		http.SetOperation(ctx, OperationArticleDeleteArticle)
		h := ctx.Middleware(func(ctx context.Context, req interface{}) (interface{}, error) {
			return srv.DeleteArticle(ctx, req.(*DeleteArticleRequest))
		})
		out, err := h(ctx, &in)
		if err != nil {
			return err
		}
		reply := out.(*DeleteArticleReply)
		return ctx.Result(200, reply)
	}
}

func _Article_GetArticle0_HTTP_Handler(srv ArticleHTTPServer) func(ctx http.Context) error {
	return func(ctx http.Context) error {
		var in GetArticleRequest
		if err := ctx.BindQuery(&in); err != nil {
			return err
		}
		if err := ctx.BindVars(&in); err != nil {
			return err
		}
		http.SetOperation(ctx, OperationArticleGetArticle)
		h := ctx.Middleware(func(ctx context.Context, req interface{}) (interface{}, error) {
			return srv.GetArticle(ctx, req.(*GetArticleRequest))
		})
		out, err := h(ctx, &in)
		if err != nil {
			return err
		}
		reply := out.(*GetArticleReply)
		return ctx.Result(200, reply)
	}
}

func _Article_ListArticle0_HTTP_Handler(srv ArticleHTTPServer) func(ctx http.Context) error {
	return func(ctx http.Context) error {
		var in ListArticleRequest
		if err := ctx.BindQuery(&in); err != nil {
			return err
		}
		http.SetOperation(ctx, OperationArticleListArticle)
		h := ctx.Middleware(func(ctx context.Context, req interface{}) (interface{}, error) {
			return srv.ListArticle(ctx, req.(*ListArticleRequest))
		})
		out, err := h(ctx, &in)
		if err != nil {
			return err
		}
		reply := out.(*ListArticleReply)
		return ctx.Result(200, reply)
	}
}

type ArticleHTTPClient interface {
	CreateArticle(ctx context.Context, req *CreateArticleRequest, opts ...http.CallOption) (rsp *CreateArticleReply, err error)
	DeleteArticle(ctx context.Context, req *DeleteArticleRequest, opts ...http.CallOption) (rsp *DeleteArticleReply, err error)
	GetArticle(ctx context.Context, req *GetArticleRequest, opts ...http.CallOption) (rsp *GetArticleReply, err error)
	ListArticle(ctx context.Context, req *ListArticleRequest, opts ...http.CallOption) (rsp *ListArticleReply, err error)
	UpdateArticle(ctx context.Context, req *UpdateArticleRequest, opts ...http.CallOption) (rsp *UpdateArticleReply, err error)
}

type ArticleHTTPClientImpl struct {
	cc *http.Client
}

func NewArticleHTTPClient(client *http.Client) ArticleHTTPClient {
	return &ArticleHTTPClientImpl{client}
}

func (c *ArticleHTTPClientImpl) CreateArticle(ctx context.Context, in *CreateArticleRequest, opts ...http.CallOption) (*CreateArticleReply, error) {
	var out CreateArticleReply
	pattern := "/newssub/v1/article/create"
	path := binding.EncodeURL(pattern, in, false)
	opts = append(opts, http.Operation(OperationArticleCreateArticle))
	opts = append(opts, http.PathTemplate(pattern))
	err := c.cc.Invoke(ctx, "POST", path, in, &out, opts...)
	if err != nil {
		return nil, err
	}
	return &out, nil
}

func (c *ArticleHTTPClientImpl) DeleteArticle(ctx context.Context, in *DeleteArticleRequest, opts ...http.CallOption) (*DeleteArticleReply, error) {
	var out DeleteArticleReply
	pattern := "/newssub/v1/article/{uid}"
	path := binding.EncodeURL(pattern, in, true)
	opts = append(opts, http.Operation(OperationArticleDeleteArticle))
	opts = append(opts, http.PathTemplate(pattern))
	err := c.cc.Invoke(ctx, "DELETE", path, nil, &out, opts...)
	if err != nil {
		return nil, err
	}
	return &out, nil
}

func (c *ArticleHTTPClientImpl) GetArticle(ctx context.Context, in *GetArticleRequest, opts ...http.CallOption) (*GetArticleReply, error) {
	var out GetArticleReply
	pattern := "/newssub/v1/article/{uid}"
	path := binding.EncodeURL(pattern, in, true)
	opts = append(opts, http.Operation(OperationArticleGetArticle))
	opts = append(opts, http.PathTemplate(pattern))
	err := c.cc.Invoke(ctx, "GET", path, nil, &out, opts...)
	if err != nil {
		return nil, err
	}
	return &out, nil
}

func (c *ArticleHTTPClientImpl) ListArticle(ctx context.Context, in *ListArticleRequest, opts ...http.CallOption) (*ListArticleReply, error) {
	var out ListArticleReply
	pattern := "/newssub/v1/article/list"
	path := binding.EncodeURL(pattern, in, true)
	opts = append(opts, http.Operation(OperationArticleListArticle))
	opts = append(opts, http.PathTemplate(pattern))
	err := c.cc.Invoke(ctx, "GET", path, nil, &out, opts...)
	if err != nil {
		return nil, err
	}
	return &out, nil
}

func (c *ArticleHTTPClientImpl) UpdateArticle(ctx context.Context, in *UpdateArticleRequest, opts ...http.CallOption) (*UpdateArticleReply, error) {
	var out UpdateArticleReply
	pattern := "/newssub/v1/article/{uid}"
	path := binding.EncodeURL(pattern, in, false)
	opts = append(opts, http.Operation(OperationArticleUpdateArticle))
	opts = append(opts, http.PathTemplate(pattern))
	err := c.cc.Invoke(ctx, "PUT", path, in, &out, opts...)
	if err != nil {
		return nil, err
	}
	return &out, nil
}
