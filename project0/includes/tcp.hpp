#ifndef PROJECT0_SOCKET_H
#define PROJECT0_SOCKET_H
#include <WS2tcpip.h>
#include <WinSock2.h>

#include <string>

#pragma comment(lib, "Ws2_32.lib")
#include <iostream>
namespace project0
{
class Tcp
{
 public:
    struct RAIIAddrinfo
    {
        addrinfo* value;
        RAIIAddrinfo(addrinfo* value) : value(value)
        {
            // Do nothing
        }
        ~RAIIAddrinfo()
        {
            freeaddrinfo(value);
        }
    };
    Tcp();
    ~Tcp();
    void init();
    void connect(const std::string& host, const int port);
    void disconnect();
    void send(const std::string& payload);
    void send(const char* payload, int size);
    void accept(const Tcp& tcp);
    std::string recv();
    RAIIAddrinfo dns_resolve(const std::string& host, const int port) const;
    SOCKET socket = INVALID_SOCKET;

 private:
    int port;
    static constexpr int buffer_size = 1024;
};
}  // namespace project0
#endif  // PROJECT0_SOCKET_H