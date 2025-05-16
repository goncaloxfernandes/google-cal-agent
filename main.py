from calendar_lc import init_lc, execute_query
from listener import wait_for_wake_word, init_listener, listen_to_command
from speaker import init_speaker, speak

if __name__=='__main__':
    init_lc()
    init_listener()
    init_speaker()

    while True:
        wait_for_wake_word()
        command = listen_to_command()
        answer = execute_query(command)
        speak(answer)
        