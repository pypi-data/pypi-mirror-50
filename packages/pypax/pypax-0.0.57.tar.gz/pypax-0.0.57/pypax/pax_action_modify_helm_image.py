from .pax_action import PaxAction
import os
from logkit import log
import yaml
from typing import Union
import re


class PaxActionModifyHelmImage(PaxAction):
    
    HELM_VALUES_FILE_KEY = "HELM_VALUES_FILE"
    ECR_REPO_KEY = "ECR_REPO"
    DOCKER_IMAGE_KEY = "DOCKER_IMAGE"
    COMMIT_TAG_FILE = ".pax/commit_hash"

    def get_docker_tag(self):
        """ Extract the Docker commit tag from the local file system. """
        tag = None
        with open(self.COMMIT_TAG_FILE, "r") as f:
            tag = f.read()
        
        tag = tag.strip().replace("\n", "")
        log.info("Got Docker Tag", {"tag": tag})
        return tag

    def get_docker_image(self, env_map: dict):
        """ Extract the Docker repo/image from the ENV vars. """
        repo = env_map[self.ECR_REPO_KEY]
        image = env_map[self.DOCKER_IMAGE_KEY]
        full_repo_path = "{}/{}".format(repo, image)
        log.info("Got Docker Repo", {"repo": full_repo_path})
        return full_repo_path

    def execute(self, env_map: Union[dict, None]=None):
        
        values_file = env_map[self.HELM_VALUES_FILE_KEY]  # "./fake_helm/values.fake.yaml"  # env_map["HELM_VALUES_FILE"]
        log.info("Helm Values File", {
            "path": values_file
        })

        # Attempt to update values file.
        if not os.path.exists(values_file):
            log.error("Values File Not Found!", {
                "file": values_file
            })
            raise Exception("BOOM")

        replace_data = {
            "repository": self.get_docker_image(env_map),
            "tag": self.get_docker_tag()
        }

        # Attempt line-by-line update to keep the rest of the file stable.
        with open(values_file, "r") as f:
            lines = f.readlines()

        with open("./fake_helm/values.out.yaml", "w") as f:
            
            under_image = False
            image_modified = False

            for line in lines:

                line_written = False

                if not under_image and not image_modified:
                    is_image = re.search("^image:", line)
                    if is_image:
                        under_image = True
                else:
                    if under_image:
                        # We either find a matching line, or we break the pattern.
                        is_attribute = re.search("^ ", line) is not None
                        if is_attribute:
                            attribute_heading = line.split(":")[0]
                            attribute_name = attribute_heading.strip()
                            print("Got Attribute: ", attribute_name)
                            if attribute_name in replace_data:
                                replace_str = "{}: {}\n".format(attribute_heading, replace_data[attribute_name])
                                f.write(replace_str)
                                line_written = True
                        else:
                            under_image = False
                            image_modified = True

                if not line_written:
                    f.write(line)

        result = "Helm Chart Updated"

        self.log_results(
            self.name, 
            "<REDACTED>", 
            result)
