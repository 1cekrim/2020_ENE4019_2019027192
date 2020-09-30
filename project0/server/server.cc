#include <iostream>
#include <sstream>
#include <string>
#include <tcp.hpp>

int main()
{
    std::cout << "server start\n";

    std::string host = "localhost";
    constexpr auto port = 10000;

    std::cout << host << ':' << port << '\n';

    using namespace project0;
    Tcp tcp;
    tcp.init();

    Tcp::RAIIAddrinfo addrinfo = tcp.dns_resolve(host, port);
    auto serverAddr = addrinfo.value->ai_addr;
    auto serverAddrLen = static_cast<int>(addrinfo.value->ai_addrlen);
    auto bindResult = bind(tcp.socket, serverAddr, serverAddrLen);

    auto listenResult = listen(tcp.socket, 5);

    if (bindResult == -1 || listenResult == -1)
    {
        std::cout << "TCP 서버를 만들지 못했습니다.\n";
        return -1;
    }

    while (true)
    {
        Tcp clientTcp;
        std::cout << "accept 대기중...\n";
        clientTcp.accept(tcp);
        std::cout << "연결됨\n";
        std::string recv;

        try
        {
            recv = clientTcp.recv();
        }
        catch (std::runtime_error err)
        {
            std::cout << err.what() << '\n';
            continue;
        }

        std::cout << "[recv]\n" << recv << '\n';

        std::stringstream ss;

        ss << "hello. your message:\n" << recv << '\n';

        clientTcp.send(ss.str());
    }

    return 0;
}