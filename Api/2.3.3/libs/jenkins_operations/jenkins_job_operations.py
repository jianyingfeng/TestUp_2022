from util.core import Operation
from libs.jenkins_api.jenkins_job_api import JenkinsJobApi
from util.core import Result


# Job业务类
class JenkinsJobOperation(Operation, JenkinsJobApi):

    # 获取job名称列表
    def get_all_job_name(self):
        r = self.list_jobs()
        # print(r.raw_response.request.headers)
        job = [i['name'] for i in r.body['jobs']]
        return job

    # 获取job名称、url列表
    def get_all_job_name_with_url(self):
        r = self.list_jobs('name,url')
        job = {i['name']: i['url'] for i in r.body['jobs']}
        return job

    # 删除所有job
    def delete_all_jobs(self):
        jobs_names = self.get_all_job_name()
        for name in jobs_names:
            self.delete_job(name)
        new_jobs_names = self.get_all_job_name()
        return Result(f"{new_jobs_names} still not deleted")

    # 创建job
    def create_job_with_dsl(self, dsl, job_name):
        result = Result()
        r = self.get_job(job_name)
        if r.code == 200:
            result.success = False
            result.info = "Job Aready Exist"
            return result
        script = f"""def jobDSL=\"\"\"{dsl}\"\"\";

                       def flowDefinition = new org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition(jobDSL, true);
                       def parent = Jenkins.instance;
                       def job = new org.jenkinsci.plugins.workflow.job.WorkflowJob(parent, "{job_name}")
                       job.definition = flowDefinition
                       job.save();
                       Jenkins.instance.reload()"""
        r = self.run_groovy(script)
        r = self.get_job(job_name)
        if r.code == 200 and r.body.get('displayName') == job_name:
            result.success = True
            result.info = f"Job Created at {r.body.get('url')}"
            return result
        else:
            result.success = False
            result.info = f"Job Created failed!"
            return result
