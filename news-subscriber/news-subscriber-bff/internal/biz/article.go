package biz

import "context"

type Article struct {
	Uid     int64
	Title   string
	Content string
	Tags    []string
}

type ArticleRepo interface {
	CreateArticle(ctx context.Context, article *Article) (int64, error)
	UpdateArticle(ctx context.Context, article *Article) error
	DeleteArticle(ctx context.Context, uid int64) error
	GetArticle(ctx context.Context, uid int64) (*Article, error)
	ListArticle(ctx context.Context, start, end int64) ([]*Article, error)
}

type ArticleUsecase struct {
	repo ArticleRepo
}

func NewArticleUsecase(repo ArticleRepo) *ArticleUsecase {
	return &ArticleUsecase{repo: repo}
}
