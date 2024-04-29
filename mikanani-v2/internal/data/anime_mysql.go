package data

import (
	"context"
	"mikanani-v2/internal/biz"
	"mikanani-v2/internal/data/ent"
	"mikanani-v2/internal/data/ent/animemeta"
	"time"

	"github.com/go-kratos/kratos/v2/log"
)

const (
	ListAll = 1 + iota
	ListActive
	ListInactive
)

type animeMetaRepo struct {
	data *Data
	log  *log.Helper
}

func NewAnimeMetaRepo(data *Data, logger log.Logger) biz.AnimeMetaRepo {
	return &animeMetaRepo{
		data: data,
		log:  log.NewHelper(logger),
	}
}

func (amrp *animeMetaRepo) Count(ctx context.Context) (int64, error) {
	count, err := amrp.data.mysqlDb.AnimeMeta.Query().Count(ctx)
	return int64(count), err
}

func (amrp *animeMetaRepo) List(ctx context.Context, start, end, mode int64) ([]*biz.AnimeMeta, error) {
	pageSize := end - start + 1
	res := make([]*biz.AnimeMeta, 0)
	var data []*ent.AnimeMeta
	var err error

	if mode == ListAll {
		data, err = amrp.data.mysqlDb.AnimeMeta.Query().
			Limit(int(pageSize)).
			Offset(int((start - 1) * pageSize)).
			All(ctx)
	} else if mode == ListActive {
		data, err = amrp.data.mysqlDb.AnimeMeta.Query().
			Where(animemeta.IsActiveEQ(true)).
			Limit(int(pageSize)).
			Offset(int((start - 1) * pageSize)).
			All(ctx)
	} else if mode == ListInactive {
		data, err = amrp.data.mysqlDb.AnimeMeta.Query().
			Where(animemeta.IsActiveEQ(false)).
			Limit(int(pageSize)).
			Offset(int((start - 1) * pageSize)).
			All(ctx)
	}

	if err != nil {
		return nil, err
	}

	for _, dbMeta := range data {
		var activeStatus int32
		if dbMeta.IsActive {
			activeStatus = 1
		} else {
			activeStatus = 0
		}
		res = append(res, &biz.AnimeMeta{
			Id:             int64(dbMeta.ID),
			Uid:            int64(dbMeta.UID),
			Name:           dbMeta.Name,
			DownloadBitMap: dbMeta.DownloadBitmap,
			IsActive:       activeStatus,
			Tags:           dbMeta.Tags,
		})
	}
	return res, nil
}

func (amrp *animeMetaRepo) Insert(ctx context.Context, meta *biz.AnimeMeta) error {
	isActive := false
	if meta.IsActive > 0 {
		isActive = true
	}
	_, err := amrp.data.mysqlDb.AnimeMeta.Create().
		SetUID(meta.Uid).
		SetName(meta.Name).
		SetDownloadBitmap(meta.DownloadBitMap).
		SetIsActive(isActive).
		SetTags(meta.Tags).
		Save(ctx)

	if err == nil {
		amrp.log.Infof("[animeMetaRepo.Insert][uid-%d]success.", meta.Uid)
	}

	return err
}

func (amrp *animeMetaRepo) Update(ctx context.Context, meta *biz.AnimeMeta) error {
	isActive := false
	if meta.IsActive > 0 {
		isActive = true
	}
	_, err := amrp.data.mysqlDb.AnimeMeta.Update().
		Where(animemeta.UIDEQ(meta.Uid)).
		SetUpdateTime(time.Now()).
		SetName(meta.Name).
		SetDownloadBitmap(meta.DownloadBitMap).
		SetIsActive(isActive).
		Save(ctx)

	if err == nil {
		amrp.log.Infof("[animeMetaRepo.Update][uid-%d]success.", meta.Uid)
	}
	return nil
}

func (amrp *animeMetaRepo) QueryByUid(ctx context.Context, uid int64) (*biz.AnimeMeta, error) {
	meta, err := amrp.data.mysqlDb.AnimeMeta.Query().
		Where(animemeta.UIDEQ(uid)).
		Only(ctx)
	if err != nil {
		return nil, err
	}

	var isActive int32
	if meta.IsActive {
		isActive = 1
	} else {
		isActive = 0
	}

	return &biz.AnimeMeta{
		Uid:            meta.UID,
		Name:           meta.Name,
		DownloadBitMap: meta.DownloadBitmap,
		IsActive:       isActive,
		Tags:           meta.Tags,
	}, nil
}

func (amrp *animeMetaRepo) Delete(ctx context.Context, uid int64) error {
	_, err := amrp.data.mysqlDb.AnimeMeta.Delete().
		Where(animemeta.UIDEQ(uid)).
		Exec(ctx)
	if err == nil {
		amrp.log.Infof("[animeMetaRepo.Delete][uid-%d]success.", uid)
	}
	return err
}
