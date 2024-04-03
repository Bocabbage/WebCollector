package service

import (
	"context"

	pb "news-subscriber-bff/api/newssub/v1"
	"news-subscriber-bff/internal/biz"
	"news-subscriber-bff/internal/conf"
	"news-subscriber-bff/internal/data/ent"

	"github.com/bwmarrin/snowflake"
	"github.com/go-kratos/kratos/v2/log"
)

type ArticleService struct {
	pb.UnimplementedArticleServer
	articleUc *biz.ArticleUsecase
	log       *log.Helper
	nodeId    int64
}

func NewArticleService(conf *conf.Utils, articleUc *biz.ArticleUsecase, logger log.Logger) *ArticleService {
	return &ArticleService{
		articleUc: articleUc,
		log:       log.NewHelper(logger),
		nodeId:    conf.SnowflakeId,
	}
}

func (s *ArticleService) CreateArticle(ctx context.Context, req *pb.CreateArticleRequest) (*pb.CreateArticleReply, error) {
	node, err := snowflake.NewNode(s.nodeId)
	if err != nil {
		s.log.Error("[create][error]snowflake new node: %v", err)
		return nil, err
	}

	newArticle := &biz.Article{
		Uid:   node.Generate().Int64(),
		Title: req.Title,
		Tags:  req.Tags,
	}
	err = s.articleUc.Create(ctx, newArticle)
	if err != nil {
		s.log.Error("[create][error]uid: %d, title: %s, error: %v", newArticle.Uid, newArticle.Title, err)
		return nil, err
	}
	s.log.Info("[create][success]uid: %d, title: %s", newArticle.Uid, newArticle.Title)
	return &pb.CreateArticleReply{Uid: newArticle.Uid}, err
}

func (s *ArticleService) UpdateArticle(ctx context.Context, req *pb.UpdateArticleRequest) (*pb.UpdateArticleReply, error) {
	updateArticle := &biz.Article{
		Uid:   req.Uid,
		Title: req.Title,
		Tags:  req.Tags,
	}
	err := s.articleUc.Update(ctx, updateArticle)
	if err != nil {
		s.log.Error("[update][error]uid: %d, error: %v", updateArticle.Uid, err)
		return nil, err
	}
	s.log.Info("[update][success]uid: %d, title: %s", updateArticle.Uid, updateArticle.Title)
	return &pb.UpdateArticleReply{}, nil
}

func (s *ArticleService) DeleteArticle(ctx context.Context, req *pb.DeleteArticleRequest) (*pb.DeleteArticleReply, error) {
	err := s.articleUc.Delete(ctx, req.Uid)
	if err != nil {
		s.log.Error("[delete][error]uid: %d, error: %v", req.Uid, err)
		return nil, err
	}
	s.log.Info("[delete][success]uid: %d", req.Uid)
	return &pb.DeleteArticleReply{}, nil
}

func (s *ArticleService) GetArticle(ctx context.Context, req *pb.GetArticleRequest) (*pb.GetArticleReply, error) {
	article, err := s.articleUc.Get(ctx, req.Uid)
	if err != nil {
		s.log.Error("[get][error]uid: %d, error: %v", req.Uid, err)
		// return nil, err
		// TODO: enhance error-code check & use
		if ent.IsNotFound(err) {
			return nil, pb.ErrorArticleNotFound("uid: %d article not in database", req.Uid)
		}
		return nil, pb.ErrorInternalError("uid: %d gather failed - internal error", req.Uid)
	}
	return &pb.GetArticleReply{Article: &pb.ArticleItem{
		Uid:     article.Uid,
		Title:   article.Title,
		Content: article.Content,
		Tags:    article.Tags,
	}}, nil
}

func (s *ArticleService) ListArticle(ctx context.Context, req *pb.ListArticleRequest) (*pb.ListArticleReply, error) {
	articles, err := s.articleUc.List(ctx, req.Start, req.End)
	if err != nil {
		s.log.Error("[list][error]start: %d, end: %d, error: %v", req.Start, req.End, err)
		return nil, err
	}

	articleItems := make([]*pb.ArticleItem, 0)
	for _, art := range articles {
		articleItems = append(articleItems, &pb.ArticleItem{
			Uid:     art.Uid,
			Title:   art.Title,
			Content: art.Content,
			Tags:    art.Tags,
		})
	}

	return &pb.ListArticleReply{
		Articles: articleItems,
	}, nil
}
