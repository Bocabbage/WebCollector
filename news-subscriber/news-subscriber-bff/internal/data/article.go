package data

import (
	"context"
	"news-subscriber-bff/internal/biz"

	"github.com/go-kratos/kratos/v2/log"
)

type articleRepo struct {
	data *Data
	log  *log.Helper
}

func NewArticleRepo(data *Data, logger log.Logger) biz.ArticleRepo {
	return &articleRepo{
		data: data,
		log:  log.NewHelper(logger),
	}
}

// TODO: impl
func (rp *articleRepo) CreateArticle(ctx context.Context, article *biz.Article) (int64, error) {
	return 0, nil
}
func (rp *articleRepo) UpdateArticle(ctx context.Context, article *biz.Article) error {
	return nil
}
func (rp *articleRepo) DeleteArticle(ctx context.Context, uid int64) error {
	return nil
}
func (rp *articleRepo) GetArticle(ctx context.Context, uid int64) (*biz.Article, error) {
	return &biz.Article{}, nil
}
func (rp *articleRepo) ListArticle(ctx context.Context, start, end int64) ([]*biz.Article, error) {
	return make([]*biz.Article, 0), nil
}
