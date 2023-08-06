from typing import Dict, List, Union

from .client import Client


class PivotalTracker:

    base_url = 'https://www.pivotaltracker.com/services/v5'

    def __init__(self, token: str = ''):
        if not token:
            raise Exception('Please provide your api token')
        self.token: str = token
        headers: Dict['str', 'str'] = {'Content-Type': 'application/json', 'X-TrackerToken': token}
        self.__client: Client = Client(headers=headers)

    def get_story(self, story_id: Union[str, int], project_id: Union[str, int]) -> Dict:
        url: str = f'{self.base_url}/projects/{project_id}/stories/{story_id}'
        story: Dict = self.__client.get(url)
        return story

    def get_story_list(self, project_id: Union[str, int]) -> List[Dict]:
        url: str = f'{self.base_url}/projects/{project_id}/stories/'
        stories: List[Dict] = self.__client.get(url)
        return stories

    def get_project(self, project_id: Union[str, int]) -> Dict:
        url: str = f'{self.base_url}/projects/{project_id}'
        project: Dict = self.__client.get(url)
        return project

    def get_project_list(self) -> List[Dict]:
        url: str = f'{self.base_url}/projects/'
        projects: List[Dict] = self.__client.get(url)
        return projects

    def get_iteration_list(self, project_id: Union[str, int], limit: Union[str, int] = 10,
                           offset: Union[str, int] = 0) -> List[Dict]:
        url: str = f'{self.base_url}/projects/{project_id}/iterations'
        iterations: List[Dict] = self.__client.get(url, params={'limit': limit, 'offset': offset})
        return iterations

    def get_project_membership_list(self, project_id: Union[str, int]) -> Dict:
        url: str = f'{self.base_url}/projects/{project_id}/memberships'
        memberships: Dict = self.__client.get(url)
        return memberships

    def get_account_list(self) -> List[Dict]:
        url: str = f'{self.base_url}/accounts'
        accounts: List[Dict] = self.__client.get(url)
        return accounts

    def get_project_label_list(self, project_id: Union[str, int]) -> List[Dict]:
        url: str = f'{self.base_url}/projects/{project_id}/labels'
        labels: List[Dict] = self.__client.get(url)
        return labels

    def get_story_owner_list(self, story_id: Union[str, int], project_id: Union[str, int]) -> List[Dict]:
        url: str = f'{self.base_url}/projects/{project_id}/stories/{story_id}/owners'
        owners: List[Dict] = self.__client.get(url)
        return owners

    def get_story_task_list(self, story_id: Union[str, int], project_id: Union[str, int]) -> List[Dict]:
        url: str = f'{self.base_url}/projects/{project_id}/stories/{story_id}/tasks'
        tasks: List[Dict] = self.__client.get(url)
        return tasks

    def get_story_comment_list(self, story_id: Union[str, int], project_id: Union[str, int]) -> List[Dict]:
        url: str = f'{self.base_url}/projects/{project_id}/stories/{story_id}/comments'
        comments: List[Dict] = self.__client.get(url)
        return comments

    def get_story_comment(self, story_id: Union[str, int], project_id: Union[str, int],
                          comment_id: Union[str, int]) -> Dict:
        url: str = f'{self.base_url}/projects/{project_id}/stories/{story_id}/comments/{comment_id}'
        comment: Dict = self.__client.get(url)
        return comment

    def get_story_task(self, story_id: Union[str, int], project_id: Union[str, int],
                       task_id: Union[str, int]) -> Dict:
        url: str = f'{self.base_url}/projects/{project_id}/stories/{story_id}/tasks/{task_id}'
        task: Dict = self.__client.get(url)
        return task

    def get_project_epic_list(self, project_id: Union[str, int]) -> List[Dict]:
        url: str = f'{self.base_url}/projects/{project_id}/epics'
        epics: List[Dict] = self.__client.get(url)
        return epics

    def get_project_epic_comment_list(self, project_id: Union[str, int],
                                      epic_id: Union[str, int]) -> List[Dict]:
        url: str = f'{self.base_url}/projects/{project_id}/epics/{epic_id}/comments'
        epic_comments: List[Dict] = self.__client.get(url)
        return epic_comments

    def get_project_epic(self, project_id: Union[str, int], epic_id: Union[str, int]) -> Dict:
        url: str = f'{self.base_url}/projects/{project_id}/epics/{epic_id}'
        epic: Dict = self.__client.get(url)
        return epic

    def post_story_label(self, project_id: Union[str, int], story_id: Union[str, int],
                         label: Union[str, int]) -> Dict:
        url: str = f'{self.base_url}/projects/{project_id}/stories/{story_id}/labels'
        data: Dict[str, str] = {'name': label, }
        labels: Dict = self.__client.post(url, data=data)
        return labels

    def post_story(self, project_id: Union[str, int], name: Union[str, int], description: Union[str, int],
                   story_type: Union[str, int] = 'feature', **kwargs) -> Dict:
        url: str = f'{self.base_url}/projects/{project_id}/stories'
        data: Dict = {'name': name, 'description': description, 'story_type': story_type, **kwargs}
        story: Dict = self.__client.post(url, data=data)
        return story

    def post_story_comment(self, project_id: Union[str, int], story_id: Union[str, int],
                           comment: Union[str, int]) -> Dict:
        url: str = f'{self.base_url}/projects/{project_id}/stories/{story_id}/comments'
        data: Dict[str, str] = {'text': comment, }
        comment: Dict = self.__client.post(url, data=data)
        return comment

    def edit_story(self, project_id: Union[str, int], story_id: Union[str, int], **kwargs) -> Dict:
        url: str = f'{self.base_url}/projects/{project_id}/stories/{story_id}'
        edit_story: Dict = self.__client.put(url, data=kwargs)
        return edit_story

    def delete_story(self, project_id: Union[str, int], story_id: Union[str, int]):
        url: str = f'{self.base_url}/projects/{project_id}/stories/{story_id}'
        self.__client.delete(url)

    def delete_comment(self, project_id: Union[str, int], story_id: Union[str, int],
                       comment_id: Union[str, int]):
        url: str = f'{self.base_url}/projects/{project_id}/stories/{story_id}/comments/{comment_id}'
        self.__client.delete(url)

    def delete_story_label(self, project_id: Union[str, int], story_id: Union[str, int],
                           label_id: Union[str, int]):
        url: str = f'{self.base_url}/projects/{project_id}/stories/{story_id}/labels/{label_id}'
        self.__client.delete(url)

    def get_story_review_list(self, project_id: Union[str, int], story_id: Union[str, int]) -> List:
        url: str = f'{self.base_url}/projects/{project_id}/stories/{story_id}/reviews'
        reviews: List = self.__client.get(url)
        return reviews

    def post_story_review(self, project_id: Union[str, int], story_id: Union[str, int],
                          review_type_id: Union[str, int], **kwargs) -> Dict:
        url: str = f'{self.base_url}/projects/{project_id}/stories/{story_id}/reviews'
        data: Dict = {'review_type_id': review_type_id, **kwargs}
        review: Dict = self.__client.post(url, data=data)
        return review

    def get_story_review(self, project_id: Union[str, int], story_id: Union[str, int],
                         review_id: Union[str, int]) -> Dict:
        url: str = f'{self.base_url}/projects/{project_id}/stories/{story_id}/reviews/{review_id}'
        review: Dict = self.__client.get(url)
        return review

    def edit_story_review(self, project_id: Union[str, int], story_id: Union[str, int],
                          review_id: Union[str, int], **kwargs) -> Dict:
        url: str = f'{self.base_url}/projects/{project_id}/stories/{story_id}/reviews/{review_id}'
        data: Dict = kwargs
        review: Dict = self.__client.put(url=url, data=data)
        return review

    def delete_story_review(self, project_id: Union[str, int], story_id: Union[str, int], review_id: Union[str, int]):
        url: str = f'{self.base_url}/projects/{project_id}/stories/{story_id}/reviews/{review_id}'
        self.__client.delete(url)
