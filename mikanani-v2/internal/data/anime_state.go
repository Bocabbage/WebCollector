package data

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"mikanani-v2/internal/biz"
	"strconv"
	"time"

	"github.com/go-kratos/kratos/v2/log"
)

var recentUpdateKey string

func init() {
	recentUpdateKeyHash := sha256.Sum256([]byte("mikananistate:recentupdate"))
	recentUpdateKey = hex.EncodeToString(recentUpdateKeyHash[:])
}

type animeStateRepo struct {
	data *Data
	log  *log.Helper
}

func NewAnimeStateRepo(data *Data, logger log.Logger) biz.AnimeStateRepo {
	return &animeStateRepo{
		data: data,
		log:  log.NewHelper(logger),
	}
}

func (asrp *animeStateRepo) GetRecentUpdateList(ctx context.Context) (*[]int64, error) {
	// redis hash: hash256(mikananistate:recentupdate) uid expired-timestamp
	res, err := asrp.data.redisCli.HGetAll(ctx, recentUpdateKey).Result()
	if err != nil {
		return nil, err
	}
	uids := make([]int64, 0)
	for k, v := range res {
		expTime, _ := strconv.ParseInt(v, 10, 64)
		now := time.Now().Unix()
		if now < expTime {
			uid, _ := strconv.ParseInt(k, 10, 64)
			uids = append(uids, uid)
		}
	}
	return &uids, nil
}

func (asrp *animeStateRepo) DeleteRecentUpdateById(ctx context.Context, uid int64) error {
	if err := asrp.data.redisCli.HDel(ctx, recentUpdateKey, fmt.Sprintf("%d", uid)).Err(); err != nil {
		asrp.log.Errorf("[animeStateRepo.DeleteRecentUpdateById]Error: %v", err)
		return err
	}
	return nil
}
