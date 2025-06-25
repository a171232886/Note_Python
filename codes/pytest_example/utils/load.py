import os
import yaml


def load_test_case():
    folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
    test_case_name_list = [name for name in os.listdir(folder_path) if name.endswith(".yaml")]
    
    test_case_list = []
    for test_case_name in test_case_name_list:
        test_case_path = os.path.join(folder_path, test_case_name)
        with open(test_case_path, "r", encoding="utf-8") as file:
            test_case = yaml.safe_load(file)
            steps = test_case.get("steps", [])
            test_case_list.append(
                ( steps.get("send", []), steps.get("validate", []), steps.get("extract", []) )
            )

    return test_case_list



if __name__ == "__main__":
    test_case_list = load_test_case()
    for request, validate, extract in test_case_list:
        print(f"Request: {request}, Validate: {validate}, Extract: {extract}")
    print("Test cases loaded successfully.")