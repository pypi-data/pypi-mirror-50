from ipykernel.kernelbase import Kernel
from scriptax_runtime.invoker import execute_string


class ScriptaxKernel(Kernel):
    implementation = 'Scriptax'
    implementation_version = '4'
    language = 'no-op'
    language_version = '4'
    language_info = {
        'name': 'Scriptax',
        'mimetype': 'text/plain',
        'file_extension': '.ah',
    }
    banner = "Scriptax kernel - Executes .ah"

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            block_status, visitor, total_time = execute_string(code=code, debug=False)

            result: str = ""

            result += "RESULT: " + str(block_status.result) + "\n\n"

            result += "Benchmark: " + str(total_time) + " seconds." + "\n\n"

            stream_content = {'name': 'stdout', 'text': result}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
                }
