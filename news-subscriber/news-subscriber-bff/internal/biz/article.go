package biz

import (
	"context"
	"time"
)

type Article struct {
	Uid        int64
	Title      string
	Content    string
	Tags       []string
	CreateTime time.Time
	UpdateTime time.Time
}

type ArticleRepo interface {
	CreateArticle(ctx context.Context, article *Article) error
	UpdateArticle(ctx context.Context, article *Article) error
	DeleteArticle(ctx context.Context, uid int64) error
	GetArticle(ctx context.Context, uid int64) (*Article, error)
	ListArticle(ctx context.Context, start, end int64) ([]*Article, error)
}

type ArticleUsecase struct {
	repo ArticleRepo
}

func (au *ArticleUsecase) Create(ctx context.Context, article *Article) error {
	return au.repo.CreateArticle(ctx, article)
}

func (au *ArticleUsecase) Update(ctx context.Context, article *Article) error {
	return au.repo.UpdateArticle(ctx, article)
}

func (au *ArticleUsecase) Delete(ctx context.Context, uid int64) error {
	return au.repo.DeleteArticle(ctx, uid)
}

func (au *ArticleUsecase) Get(ctx context.Context, uid int64) (*Article, error) {
	return au.repo.GetArticle(ctx, uid)
}

func (au *ArticleUsecase) List(ctx context.Context, start, end int64) ([]*Article, error) {
	return au.repo.ListArticle(ctx, start, end)
}

func NewArticleUsecase(repo ArticleRepo) *ArticleUsecase {
	return &ArticleUsecase{repo: repo}
}
