package service

import (
	"context"

	pb "mikanani-v2/api/mikanani/v2"
	"mikanani-v2/internal/biz"
	"mikanani-v2/internal/conf"

	"github.com/bwmarrin/snowflake"
	"github.com/go-kratos/kratos/v2/log"
	"google.golang.org/protobuf/types/known/emptypb"
)

type MikananiServiceService struct {
	pb.UnimplementedMikananiServiceServer
	auc    *biz.AnimeUsecase
	log    *log.Helper
	nodeId int64
}

func NewMikananiServiceService(conf *conf.Utils, auc *biz.AnimeUsecase, logger log.Logger) *MikananiServiceService {
	return &MikananiServiceService{
		auc:    auc,
		log:    log.NewHelper(logger),
		nodeId: conf.SnowflakeId,
	}
}

func (s *MikananiServiceService) ListAnimeMeta(ctx context.Context, req *pb.ListAnimeMetaRequest) (*pb.ListAnimeMetaResponse, error) {
	res, err := s.auc.ListAnimeMeta(
		ctx,
		req.GetStartIndex(),
		req.GetEndIndex(),
		int64(req.GetStatusFilter()),
	)
	if err != nil {
		return nil, err
	}

	resAnimeMetaList := pb.ListAnimeMetaResponse{}
	for _, meta := range res {
		resAnimeMetaList.ItemCount++
		resAnimeMetaList.AnimeMetas = append(
			resAnimeMetaList.AnimeMetas,
			&pb.AnimeMeta{
				Uid:            meta.Uid,
				Name:           meta.Name,
				DownloadBitmap: meta.DownloadBitMap,
				IsActive:       meta.IsActive,
				Tags:           meta.Tags, // TODO: enhancement
			},
		)
	}

	return &resAnimeMetaList, nil
}

func (s *MikananiServiceService) GetAnimeDoc(ctx context.Context, req *pb.GetAnimeDocRequest) (*pb.GetAnimeDocResponse, error) {
	res, err := s.auc.GetAnimeDoc(ctx, req.GetUid())
	if err != nil {
		return nil, err
	}

	resDoc := pb.AnimeDoc{
		Uid:    res.Uid,
		RssUrl: res.RssUrl,
		Rule:   res.Rule,
		Regex:  res.Regex,
	}
	return &pb.GetAnimeDocResponse{AnimeDoc: &resDoc}, nil
}

func (s *MikananiServiceService) UpdateAnimeDoc(ctx context.Context, req *pb.UpdateAnimeDocRequest) (*emptypb.Empty, error) {
	if err := s.auc.UpdateAnimeDoc(ctx, &biz.AnimeDoc{
		Uid:    req.GetUpdateAnimeDoc().GetUid(),
		RssUrl: req.GetUpdateAnimeDoc().GetRssUrl(),
		Rule:   req.GetUpdateAnimeDoc().GetRule(),
		Regex:  req.GetUpdateAnimeDoc().GetRegex(),
	}); err != nil {
		return nil, err
	}

	return &emptypb.Empty{}, nil
}

func (s *MikananiServiceService) UpdateAnimeMeta(ctx context.Context, req *pb.UpdateAnimeMetaRequest) (*emptypb.Empty, error) {
	// Strict usecase means only takes name/isactive/tags from user-input
	// This svc will be visited only from UI so some control segments like
	// [downloadBitmap] will not be updated in this API.
	if err := s.auc.UpdateAnimeMetaStrict(ctx, &biz.AnimeMeta{
		Uid:      req.GetUpdateAnimeMeta().GetUid(),
		Name:     req.GetUpdateAnimeMeta().GetName(),
		IsActive: req.GetUpdateAnimeMeta().GetIsActive(),
		Tags:     req.UpdateAnimeMeta.Tags,
	}); err != nil {
		return nil, err
	}
	return &emptypb.Empty{}, nil
}

func (s *MikananiServiceService) InsertAnimeItem(ctx context.Context, req *pb.InsertAnimeItemRequest) (*pb.InsertAnimeItemResponse, error) {

	node, err := snowflake.NewNode(s.nodeId)
	if err != nil {
		s.log.Error("[create][error]snowflake new node: %v", err)
		return nil, err
	}
	uid := node.Generate().Int64()

	newAnimeMeta := &biz.AnimeMeta{
		Uid:            uid,
		Name:           req.GetInsertAnimeMeta().GetName(),
		DownloadBitMap: 0,
		IsActive:       req.GetInsertAnimeMeta().GetIsActive(),
		Tags:           req.GetInsertAnimeMeta().GetTags(),
	}

	newAnimeDoc := &biz.AnimeDoc{
		Uid:    uid,
		RssUrl: req.GetInsertAnimeDoc().GetRegex(),
		Rule:   req.GetInsertAnimeDoc().GetRule(),
		Regex:  req.GetInsertAnimeDoc().GetRegex(),
	}

	if err := s.auc.InsertAnime(ctx, newAnimeMeta, newAnimeDoc); err != nil {
		return nil, err
	}

	return &pb.InsertAnimeItemResponse{Uid: uid}, nil
}

func (s *MikananiServiceService) DeleteAnimeItem(ctx context.Context, req *pb.DeleteAnimeItemRequest) (*emptypb.Empty, error) {
	if err := s.auc.DeleteAnimeItem(ctx, req.GetUid()); err != nil {
		return nil, err
	}
	return &emptypb.Empty{}, nil
}

func (s *MikananiServiceService) DispatchDownloadTask(ctx context.Context, req *emptypb.Empty) (*emptypb.Empty, error) {
	// TODO: impl
	return &emptypb.Empty{}, nil
}

func (s *MikananiServiceService) GetAnimeCount(ctx context.Context, req *emptypb.Empty) (*pb.GetAnimeCountResponse, error) {
	count, err := s.auc.GetAnimeCount(ctx)
	if err != nil {
		return nil, err
	}
	return &pb.GetAnimeCountResponse{Count: count}, nil
}
