#include <iostream>
#include <string>
#include <tcp.hpp>

void getInfo(std::string& host, int& port)
{
    std::cout << "host: ";
    std::cin >> host;
    std::cout << "\nport: ";
    std::cin >> port;
}

int main()
{
    std::cout << "client start\n";

    std::string host;
    int port;

    getInfo(host, port);

    std::cout << host << ':' << port << '\n';

    using namespace project0;

    Tcp tcp;

    tcp.connect(host, port);

    std::cout << "connected\nmessage: ";

    std::cin.ignore(256, '\n');
    std::string message;
    std::getline(std::cin, message);

    tcp.send(message);
    std::string recv;
    try
    {
        recv = tcp.recv();
        std::cout << "[recv]\n" << recv << '\n';
    }
    catch (std::runtime_error err)
    {
        std::cout << err.what() << '\n';
    }
    
    tcp.disconnect();

    return 0;
}