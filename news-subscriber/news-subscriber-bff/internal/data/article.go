package data

import (
	"context"
	"news-subscriber-bff/internal/biz"
	"time"

	"news-subscriber-bff/internal/data/ent"
	"news-subscriber-bff/internal/data/ent/articlemeta"

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

func (rp *articleRepo) CreateArticle(ctx context.Context, article *biz.Article) error {
	_, err := rp.data.db.ArticleMeta.
		Create().
		SetUID(article.Uid).
		SetTitle(article.Title).
		SetTags(article.Tags).
		Save(ctx)
	return err
}

func (rp *articleRepo) UpdateArticle(ctx context.Context, article *biz.Article) error {
	p, err := rp.data.db.ArticleMeta.
		Query().
		Where(articlemeta.UID(article.Uid)).
		Only(ctx)
	if err != nil {
		return err
	}
	_, err = p.
		Update().
		SetTitle(article.Title).
		SetUpdateTime(time.Now()).
		SetTags(article.Tags).
		Save(ctx)
	return err

}

func (rp *articleRepo) DeleteArticle(ctx context.Context, uid int64) error {
	_, err := rp.data.db.ArticleMeta.
		Delete().
		Where(articlemeta.UID(uid)).
		Exec(ctx)
	return err
}

func (rp *articleRepo) GetArticle(ctx context.Context, uid int64) (*biz.Article, error) {
	p, err := rp.data.db.ArticleMeta.
		Query().
		Where(articlemeta.UID(uid)).
		Only(ctx)
	if err != nil {
		return nil, err
	}
	return &biz.Article{
		Uid:        uid,
		Title:      p.Title,
		CreateTime: p.CreateTime,
		UpdateTime: p.UpdateTime,
	}, nil
}

func (rp *articleRepo) ListArticle(ctx context.Context, start, end int64) ([]*biz.Article, error) {
	res := make([]*biz.Article, 0)
	var ps []*ent.ArticleMeta
	var err error

	if end < 0 {
		// Get all
		ps, err = rp.data.db.ArticleMeta.
			Query().
			All(ctx)
	} else {
		ps, err = rp.data.db.ArticleMeta.
			Query().
			Offset(int(start - 1)).
			Limit(int(end - start)).
			All(ctx)
	}
	if err != nil {
		return nil, err
	}

	for _, p := range ps {
		res = append(res, &biz.Article{
			Uid:        p.UID,
			Title:      p.Title,
			CreateTime: p.CreateTime,
			UpdateTime: p.UpdateTime,
		})
	}

	return res, nil
}
