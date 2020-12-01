import handler

handler.template_dict = {
    './static/'
}

def main():
    handler.start_server()
    
if __name__ =="__main__":
    main()
