from time import sleep

import docker

client = docker.from_env()


def build_image(dockerfile_path, dockerfile_name, image_tag):
    try:
        print("build executed")
        client.images.build(path=dockerfile_path, dockerfile=dockerfile_name, tag=image_tag, forcerm=True)
        return True
    except Exception as err:
        print(err)
        return False


def force_installation_dockers(image_tag_list):
    for image_dict in image_tag_list:
        if image_dict["image_tag"]:
            print(image_dict["image_tag"])
            while True:
                if build_image(image_dict["path"], image_dict["dockerfile"], image_dict["image_tag"]):
                    print("build successfully on {0}".format(image_dict["image_tag"]))
                    break
                else:
                    print("on_sleep")
                    sleep(45)
        else:
            print("image exist installation skipped")
            return True
    return True

# ffuf -u https://FUZZ.rootdomain -w jhaddixall.txt -v | grep "| URL |" | awk '{print $4}'

def ffuf_subdomain_exec(local_client, domain, image_tag):
    temp = domain.split("//")
    domain_url = temp[0] + "//" + "FUZZ" + temp[1]
    try:
        resp = local_client.containers.run(image_tag,
                                           ["-u",
                                            domain_url,
                                            "-w", "/dev/shm/all.txt",
                                            "-o", "/dev/shm/out_ffuf.txt"],
                                           volumes={
                                               '/tmp/ffuf/wordlist_files': {
                                                   'bind': '/dev/shm', 'mode': 'rw'}},
                                           name=image_tag + "_isoo",
                                           auto_remove=True)
        print(resp)
        return resp
    except Exception as err:
        raise err


if __name__ == '__main__':
    def main():
        image_tag_list = [{'path': '.',
                           "dockerfile": "Dockerfile.ffuf",
                           'image_tag': 'ffuf'}
                          ]
        with open("domain_to_scan.txt", "r") as f:
            domain_name = f.read()

        if force_installation_dockers(image_tag_list):
            print("sleeped")
            sleep(3)

            ffuf_subdomain_exec(client, domain_name, "ffuf")
    main()
