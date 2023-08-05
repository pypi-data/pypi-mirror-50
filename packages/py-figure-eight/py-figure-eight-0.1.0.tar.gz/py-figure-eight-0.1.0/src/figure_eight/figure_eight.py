import os
import requests
import glog as log
import pandas as pd
from io import BytesIO, BufferedReader
import numbers


class FigureEightAPI:
    def __init__(self, api_key):
        log.debug("Creating FigureEightAPI")
        assert(isinstance(api_key, str))
        self._api_key = api_key
        self._params = (
            ("key", self._api_key),
        )
        self._base_endpoint = "https://api.figure-eight.com/v1/jobs"

    def _check_success(self, resp, error_message=None, success=200):
        if error_message is None:
            error_message = ""

        if not isinstance(error_message, str):
            error_message = str(error_message)

        if not error_message.endswith(" "):
            error_message += " "

        error_message += f"Status Code: {resp.status_code}"

        if resp.status_code != success:
            log.error(error_message)
            raise requests.exceptions.HTTPError(error_message)


class FigureEightJob(FigureEightAPI):
    def __init__(self, api_key, job_id):
        super().__init__(api_key)
        self._job_id = job_id
        self._figure_eight_json = None

    @property
    def figure_eight_json(self):
        if self._figure_eight_json is None:
            resp = requests.get(f"{self._base_endpoint}/{self._job_id}.json",
                                params=self._params)
            self._check_success(resp, f"Failed to get job {self._job_id}.")
            self._figure_eight_json = resp.json()

        return self._figure_eight_json

    def _update_parameter_data(self, data, *parameters):
        assert(all(isinstance(parameter, str) for parameter in parameters))
        assert(isinstance(data, str))
        endpoint = f"{self._base_endpoint}/{self._job_id}.json"

        params = "".join([f"[{p}]" for p in parameters])
        params = (
            *self._params,
            (f"job{params}", data)
        )
        resp = requests.put(endpoint, params)
        self._check_success(resp, (f"Failed to update {parameters}"
                                   f" for job {self._job_id}."))

    class __reset_figure_eight_job_json:
        def __init__(self, f):
            self.f = f

        def __call__(self, inst, *args, **kwargs):
            inst._figure_eight_json = None
            return self.f(inst, *args, **kwargs)

    @property
    def title(self):
        return self.figure_eight_json["title"]

    @title.setter
    @__reset_figure_eight_job_json
    def title(self, title):
        self._update_parameter_data(title, "title")

    @property
    def instructions(self):
        return self.figure_eight_json["instructions"]

    @instructions.setter
    @__reset_figure_eight_job_json
    def instructions(self, instructions):
        assert(isinstance(instructions, str))
        self._update_parameter_data(instructions, "instructions")

    @property
    def cml(self):
        return self.figure_eight_json["cml"]

    @cml.setter
    @__reset_figure_eight_job_json
    def cml(self, cml):
        assert(isinstance(cml, str))
        self._update_parameter_data(cml, "cml")

    @property
    def payment_cents(self):
        return self.figure_eight_json["payment_cents"]

    @payment_cents.setter
    @__reset_figure_eight_job_json
    def payment_cents(self, payment_cents):
        assert(isinstance(payment_cents, numbers.Number))
        self._update_parameter_data(payment_cents, "payment_cents")

    @property
    def judgments_per_unit(self):
        return self.figure_eight_json["payment_cents"]

    @judgments_per_unit.setter
    @__reset_figure_eight_job_json
    def judgments_per_unit(self, judgments_per_unit):
        assert(isinstance(judgments_per_unit, numbers.Number))
        self._update_parameter_data(judgments_per_unit, "judgments_per_unit")

    @property
    def req_ttl_in_seconds(self):
        return self.figure_eight_json["options"]["req_ttl_in_seconds"]

    @req_ttl_in_seconds.setter
    @__reset_figure_eight_job_json
    def req_ttl_in_seconds(self, req_ttl_in_seconds):
        assert(isinstance(req_ttl_in_seconds, numbers.Number))
        self._update_parameter_data(req_ttl_in_seconds,
                                    "options",
                                    "req_ttl_in_seconds")

    @property
    def units_per_assignment(self):
        return self.figure_eight_json["units_per_assignment"]

    @units_per_assignment.setter
    @__reset_figure_eight_job_json
    def units_per_assignment(self, units_per_assignment):
        assert(isinstance(units_per_assignment, numbers.Number))
        self._update_parameter_data(units_per_assignment,
                                    "units_per_assignment")

    @property
    def auto_launch(self):
        return self.figure_eight_json["auto_order"]

    @auto_launch.setter
    @__reset_figure_eight_job_json
    def auto_launch(self, auto_launch):
        assert(isinstance(auto_launch, numbers.Number))
        self._update_parameter_data(auto_launch, "auto_order")

    @property
    def id(self):
        return self._job_id

    @property
    def status(self):
        endpoint = f"{self._base_endpoint}/{self.id}/ping.json"

        resp = requests.get(endpoint, params=self._params)
        self._check_success(resp)

        return resp.json()

    def upload_csv(self, csv):
        name = "sample.csv"
        if isinstance(csv, str) and os.path.exists(csv):
            name = csv
            csv = pd.read_csv(csv)

        assert(isinstance(csv, pd.DataFrame))
        endpoint = f"{self._base_endpoint}/{self.id}/upload.json"
        headers = {
            "Content-Type": "text/csv"
        }

        params = (
            *self._params,
            ("force", True)
        )

        filelike = BytesIO(csv.to_csv(index=False).encode())
        filelike.name = name
        resp = requests.put(endpoint,
                            headers=headers,
                            params=params,
                            data=BufferedReader(filelike))
        return resp
        self._check_success(resp)

    def pause(self):
        endpoint = f"{self._base_endpoint}/{self.id}/pause.json"

        resp = requests.get(endpoint, params=self._params)
        self._check_success(resp, f"Failed to pause job {self.id}")

    def resume(self):
        endpoint = f"{self._base_endpoint}/{self.id}/resume.json"

        resp = requests.get(endpoint, params=self._params)
        self._check_success(resp, f"Failed to resume job {self.id}")

    def cancel(self):
        endpoint = f"{self._base_endpoint}/{self.id}/cancel.json"

        resp = requests.get(endpoint, params=self._params)
        self._check_success(resp, f"Failed to cancel job {self.id}")


class FigureEightClient(FigureEightAPI):
    def __init__(self, api_key):
        super().__init__(api_key)

    def create_job(self, title, instructions, cml):
        endpoint = f"{self._base_endpoint}.json"

        params = (
            *self._params,
            ("job[title]", title),
            ("job[instructions]", instructions),
            ("job[cml]", cml)
        )
        resp = requests.post(endpoint, params=params)
        self._check_success(resp, "Failed to create new job.")

        job_id = resp.json()["id"]

        return FigureEightJob(self._api_key, job_id)

    def copy_job(self, job_id, rows=None):
        assert(rows is None or rows == "gold" or rows == "all")
        endpoint = f"{self._base_endpoint}/{job_id}/copy.json"

        params = self._params
        if rows == "gold":
            params = (*params, ("gold", True))

        if rows == "all":
            params = (*params, ("all_units", True))

        resp = requests.get(endpoint, params=params)
        self._check_success(resp)

        return FigureEightJob(self._api_key, resp.json()["id"])

    def delete_job(self, job_id):
        endpoint = f"https://api.figure-eight.com/v1/jobs/{job_id}.json"

        resp = requests.delete(endpoint, params=self._params)
        # self._check_success(resp, f"Unable to delete job {job_id}")
        return resp
