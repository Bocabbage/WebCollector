package service

import (
	"context"

	pb "news-subscriber-bff/api/newssub/v1"
	"news-subscriber-bff/internal/biz"

	"github.com/go-kratos/kratos/v2/log"
)

type ArticleService struct {
	pb.UnimplementedArticleServer
	article *biz.ArticleUsecase
	log     *log.Helper
}

func NewArticleService(article *biz.ArticleUsecase, logger log.Logger) *ArticleService {
	return &ArticleService{
		article: article,
		log:     log.NewHelper(logger),
	}
}

func (s *ArticleService) CreateArticle(ctx context.Context, req *pb.CreateArticleRequest) (*pb.CreateArticleReply, error) {
	return &pb.CreateArticleReply{}, nil
}
func (s *ArticleService) UpdateArticle(ctx context.Context, req *pb.UpdateArticleRequest) (*pb.UpdateArticleReply, error) {
	return &pb.UpdateArticleReply{}, nil
}
func (s *ArticleService) DeleteArticle(ctx context.Context, req *pb.DeleteArticleRequest) (*pb.DeleteArticleReply, error) {
	return &pb.DeleteArticleReply{}, nil
}
func (s *ArticleService) GetArticle(ctx context.Context, req *pb.GetArticleRequest) (*pb.GetArticleReply, error) {
	return &pb.GetArticleReply{}, nil
}
func (s *ArticleService) ListArticle(ctx context.Context, req *pb.ListArticleRequest) (*pb.ListArticleReply, error) {
	return &pb.ListArticleReply{}, nil
}
