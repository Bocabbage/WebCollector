package server

import (
	"crypto/tls"
	v2 "mikanani-v2/api/mikanani/v2"
	"mikanani-v2/internal/conf"
	"mikanani-v2/internal/service"

	"github.com/go-kratos/kratos/v2/log"
	"github.com/go-kratos/kratos/v2/middleware/recovery"
	"github.com/go-kratos/kratos/v2/transport/grpc"
)

// NewGRPCServer new a gRPC server.
func NewGRPCServer(c *conf.Server, mikanani *service.MikananiServiceService, logger log.Logger) *grpc.Server {
	var opts = []grpc.ServerOption{
		grpc.Middleware(
			recovery.Recovery(),
		),
	}
	if c.Grpc.Network != "" {
		opts = append(opts, grpc.Network(c.Grpc.Network))
	}
	if c.Grpc.Addr != "" {
		opts = append(opts, grpc.Address(c.Grpc.Addr))
	}
	if c.Grpc.Timeout != nil {
		opts = append(opts, grpc.Timeout(c.Grpc.Timeout.AsDuration()))
	}
	if c.Tls.Cert != "" && c.Tls.Key != "" {
		cert, err := tls.LoadX509KeyPair(c.Tls.Cert, c.Tls.Key)
		if err != nil {
			log.NewHelper(logger).Warnf("Tls init failed: %v", err)
		} else {
			opts = append(opts, grpc.TLSConfig(&tls.Config{Certificates: []tls.Certificate{cert}}))
		}
	}
	srv := grpc.NewServer(opts...)
	v2.RegisterMikananiServiceServer(srv, mikanani)
	return srv
}
