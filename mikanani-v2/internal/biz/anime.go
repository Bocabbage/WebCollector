package biz

import (
	"context"

	"github.com/go-kratos/kratos/v2/log"
)

type AnimeMeta struct {
	Id             int64
	Uid            int64
	Name           string
	DownloadBitMap int64
	IsActive       int32
	Tags           []string
}

type AnimeDoc struct {
	Uid    int64
	RssUrl string
	Rule   string
	Regex  string
}

type AnimeMetaRepo interface {
	Count(ctx context.Context) (int64, error)
	List(ctx context.Context, start, end, mode int64) ([]*AnimeMeta, error)
	QueryByUid(ctx context.Context, uid int64) (*AnimeMeta, error)
	Insert(ctx context.Context, meta *AnimeMeta) error
	Update(ctx context.Context, meta *AnimeMeta) error
	Delete(ctx context.Context, uid int64) error
}

type AnimeDocRepo interface {
	QueryByUid(ctx context.Context, uid int64) (*AnimeDoc, error)
	Insert(ctx context.Context, doc *AnimeDoc) error
	Update(ctx context.Context, doc *AnimeDoc) error
	Delete(ctx context.Context, uid int64) error
}

type AnimeUsecase struct {
	log      *log.Helper
	metaRepo AnimeMetaRepo
	docRepo  AnimeDocRepo
}

func (uc *AnimeUsecase) ListAnimeMeta(ctx context.Context, start, end, mode int64) ([]*AnimeMeta, error) {
	return uc.metaRepo.List(ctx, start, end, mode)
}

func (uc *AnimeUsecase) GetAnimeDoc(ctx context.Context, uid int64) (*AnimeDoc, error) {
	return uc.docRepo.QueryByUid(ctx, uid)
}

func (uc *AnimeUsecase) UpdateAnimeDoc(ctx context.Context, doc *AnimeDoc) error {
	return uc.docRepo.Update(ctx, doc)
}

func (uc *AnimeUsecase) UpdateAnimeMeta(ctx context.Context, meta *AnimeMeta) error {
	meta, err := uc.metaRepo.QueryByUid(ctx, meta.Uid)
	return uc.metaRepo.Update(ctx, meta)
}

func (uc *AnimeUsecase) InsertAnime(ctx context.Context, meta *AnimeMeta, doc *AnimeDoc) error {
	if err := uc.metaRepo.Insert(ctx, meta); err != nil {
		uc.log.Errorf("[InsertAnime][uid:%v]insert meta info failed: %v", meta.Uid, err)
		return err
	}

	if err := uc.docRepo.Insert(ctx, doc); err != nil {
		uc.log.Errorf("[InsertAnime][uid:%v]insert doc info failed: %v", meta.Uid, err)
		// rollback meta change
		uc.metaRepo.Delete(ctx, meta.Uid)
		return err
	}

	return nil
}

func (uc *AnimeUsecase) DeleteAnimeItem(ctx context.Context, uid int64) error {
	if err := uc.metaRepo.Delete(ctx, uid); err != nil {
		uc.log.Errorf("[DeleteAnime][uid:%v]delete meta info failed: %v", uid, err)
		return err
	}

	if err := uc.docRepo.Delete(ctx, uid); err != nil {
		uc.log.Errorf("[DeleteAnime][uid:%v]delete doc info failed: %v", uid, err)
		// TODO: Add rollback
		return err
	}

	return nil
}

func (uc *AnimeUsecase) GetAnimeCount(ctx context.Context) (int64, error) {
	return uc.metaRepo.Count(ctx)
}

func NewAnimeUsecase(metaRepo AnimeMetaRepo, docRepo AnimeDocRepo, logger log.Logger) *AnimeUsecase {
	return &AnimeUsecase{
		metaRepo: metaRepo,
		docRepo:  docRepo,
		log:      log.NewHelper(logger),
	}
}
