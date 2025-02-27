from flask import (
    Blueprint,
    render_template,
    render_template_string,
    jsonify,
    request,
    session,
    url_for,
    make_response,
    redirect,
)
from platforms.platforms_module import *
import threading, time, sys, os, subprocess
from pathlib import Path
from io import StringIO
from dotenv import load_dotenv

views = Blueprint("views", __name__)
def oauth_exists():
    project_dir = Path(__file__).parent.parent
    file_path = project_dir / 'platforms' / 'oauth.json'
    if file_path.is_file():
        return True
    else:
        return False

def cache_exists():
    project_dir = Path(__file__).parent.parent
    file_path = project_dir / 'platforms' / '.cache'
    alt_path = project_dir / '.cache'
    if file_path.is_file() or alt_path.is_file():
        return True
    else:
        return False

@views.route("/erro")
def erro():
    message = request.args.get('message')
    return render_template("erro.html", message=message)

@views.route("/")
def start():
    return render_template("start.html")

@views.route("/conexao_youtube", methods=["GET", "POST"])
def conexao_youtube():
    global process
    if request.method == "GET":
        if oauth_exists() and cache_exists():
            return redirect(url_for('views.acao_render'))
        elif oauth_exists():
            return redirect(url_for('views.conexao_spotify'))
        else:
            process = None
            # Abrindo aba de autenticação web para youtube 
            if process is None:
                project_dir = Path(__file__).parent.parent
                # env_path = project_dir / 'platforms' / '.env'
                # load_dotenv(env_path)
                oauth_script = project_dir / 'platforms' / 'oauth_script.py'
                client_id = os.getenv("YT_CLIENT_ID")
                client_secret = os.getenv("YT_CLIENT_SECRET")

                process = subprocess.Popen(
                "cmd.exe",
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                # shell=True,
                cwd=str(project_dir)  
                )
        
                try:
                    # Comandos para executar em sequencia
                    commands = [
                        f"cd {project_dir}"
                        "call .\\venv\\Scripts\\activate.bat", #trocar por  call .\\Scripts\\activate em ambiente de teste
                        f"python {oauth_script} {client_id} {client_secret}"
                    ]
                    
                    # Executa comandos em sequencia
                    for cmd in commands:
                        process.stdin.write(f"{cmd}\n")
                        process.stdin.flush()  # certifica que o comando é enviado
                        time.sleep(1)
                    # para log  
                    # stdout, stderr = process.communicate()
                    # print(f"stdout: {stdout} and stderr: {stderr}")
                except Exception as e:
                    print(f"Error during OAuth process: {str(e)}")
                    raise
            
            return render_template("conexao_youtube.html")
    else:
        # Simula tecla enter no subprocesso para confirmar login youtube e carregar o arquivo oauth.json 
        process.stdin.write("\r\n\n")
        process.stdin.flush()
        time.sleep(3)  
        # para log
        # stdout, stderr = process.communicate()
        # print(f"stdout: {stdout} and stderr: {stderr}")

        try:
            process.terminate()
        except:
            process.kill()  # Force kill if termination fails
        process = None
        response = make_response("", 200)
        response.headers["HX-Redirect"] = url_for("views.conexao_spotify")
        return response
    
@views.route("/conexao_spotify", methods=["GET", "POST"])
def conexao_spotify():
    global processo
    if request.method == "GET":
        if cache_exists():
            return redirect(url_for('views.acao_render'))
        else:
            processo = None
            # Abrindo aba de autenticação web para youtube 
            if processo is None:
                project_dir = Path(__file__).parent.parent
                cache_script = project_dir / 'platforms' / 'cache_script.py'

                processo = subprocess.Popen(
                "cmd.exe",
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                # shell=True,
                cwd=str(project_dir)  
                )
        
                try:
                    # Comandos para executar em sequencia
                    commands = [
                        f"cd {project_dir}"
                        "call .\\venv\\Scripts\\activate.bat", #trocar por  call .\\Scripts\\activate em ambiente de teste
                        f"python platforms/cache_script.py"
                    ]
                    
                    # Executa comandos em sequencia
                    for cmd in commands:
                        processo.stdin.write(f"{cmd}\n")
                        processo.stdin.flush()  # certifica que o comando é enviado
                        time.sleep(1)
                    # # para log  
                    # stdout, stderr = processo.communicate()
                    # print(f"stdout: {stdout} and stderr: {stderr}")
                except Exception as e:
                    print(f"Error during OAuth process: {str(e)}")
                    raise
            
            return render_template("conexao_spotify.html")
    else:
        # Cria arquivo cache para fazer requests autenticados 
        url = request.form.get("url")
        # print(f'url: {url}')
        processo.stdin.write(f"{url}")
        processo.stdin.flush()
        time.sleep(1)  
        stdout, stderr = processo.communicate()
        print(f"stdout: {stdout} and stderr: {stderr}")

        try:
            processo.terminate()
        except:
            processo.kill()  # Force kill if termination fails
        processo = None
        return redirect(url_for('views.acao_render'))
    
@views.route("/acao_render", methods=["GET"])
def acao_render():
    if oauth_exists() and cache_exists():
        return render_template('acao.html')
    else:
        message = "Não foi possível completar autenticação, sinto muito! Se possível, tente novamente ou informe o desenvolvedor sobre o bug."
        return render_template('erro.html', message=message)


@views.route("/transfer", methods=["GET", "POST"])
def transfer():
    if request.method == "POST":
        entrada = request.form.get("entrada")
        session["entrada"] = entrada
        saida = request.form.get("saida")
        session["saida"] = saida
        return redirect(url_for("views.entrada"))
    return render_template("transfer.html")

@views.route("/entrada", methods=["GET", "POST"])
def entrada():
    if request.method == "GET":
        entrada = session.get("entrada")
        platform = get_platform(entrada)
        playlists = platform.get_playlists()
        return render_template("entrada.html", playlists=playlists, entrada=entrada)
    else:
        session["transfer_playlist"] = request.form.get("playlist")
        return render_template("end_transfer.html")

@views.route("/end_transfer", methods=["POST"])
def end_transfer():
    playlist = session.get("transfer_playlist")
    entrada = session.get("entrada")
    saida = session.get("saida")
    if not playlist or not entrada or not saida:
        print(f"playlist: {playlist} - entrada: {entrada} - saida: {saida}")
        message = "Ocorreu um erro no final da transferência. Pedimos desculpa e iremos trabalhar para arrumar."
        return render_template("erro_swap.html", message=message)

    new_playlist_name = playlist + "_yourplaylist"
    source = get_platform(entrada)
    output = get_platform(saida)
    try:
        songs_source = source.get_songs(playlist)
        output_songs_ids = output.get_songs_id(songs_source)
        output.new_playlist(new_playlist_name, output_songs_ids)
        # retornando html em caso de sucesso na transferencia
        success_html = """
        <div class="text-center space-y-4">
            <div class="text-2xl font-bold text-white mb-4">
                ✨ Transferência Completa! ✨
            </div>
            <p class="text-white mb-6">
                Sua playlist foi criada com sucesso com o nome '{}'
            </p>
            <a href="/" 
            class="inline-block px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                Voltar
            </a>
        </div>
        """.format(
            new_playlist_name
        )
        return success_html
    except Exception as e:
        message = "Desculpe-nos, ocorreu um erro no final da transferência. Avise o desenvolvedor e iremos trabalhar para arrumar."
        return render_template("erro_swap.html", message=message)

@views.route("/synchronize", methods=["GET", "POST"])
def synchronize():
    if request.method == "POST":
        primeira = request.form.get("primeira")
        session["primeira"] = primeira
        segunda = request.form.get("segunda")
        session["segunda"] = segunda
        return redirect(url_for("views.choose_playlists"))
    return render_template("sync.html")


@views.route("/choose_playlists", methods=["GET", "POST"])
def choose_playlists():
    if request.method == "GET":
        primeira = session.get("primeira")
        segunda = session.get("segunda")
        plat_1 = get_platform(primeira)
        plat_2 = get_platform(segunda)
        play_plat_1 = plat_1.get_playlists()
        play_plat_2 = plat_2.get_playlists()
        return render_template(
            "choose_playlists.html",
            play_1=play_plat_1,
            play_2=play_plat_2,
            primeira=primeira,
            segunda=segunda,
        )
    else:
        session['primeira_playlist'] = request.form.get('primeira_playlist')
        session['segunda_playlist'] = request.form.get('segunda_playlist')
        return render_template('end_sync.html')

@views.route('/end_sync', methods=['POST'])
def end_sync():
    primeira = session.get("primeira")
    segunda = session.get("segunda")
    play_1 = session.get('primeira_playlist')
    play_2 = session.get('segunda_playlist')
    plat_1 = get_platform(primeira)
    plat_2 = get_platform(segunda)
    try:
        primeira_playlist = plat_1.get_songs(play_1)
        p_play_names = get_songs_names(primeira_playlist)
        segunda_playlist = plat_2.get_songs(play_2)
        s_play_names = get_songs_names(segunda_playlist)

        p_add = []
        for name in s_play_names:
            if not is_song_in_list(name, p_play_names):
                p_add.append(name)
        
        s_add = []
        for name in p_play_names:
            if not is_song_in_list(name, s_play_names):
                s_add.append(name)
        
        p_play_songs_to_add = {'tracks': []}
        for track in segunda_playlist['tracks']:
            for name in p_add:
                if is_equal(track['name'], name):
                    p_play_songs_to_add['tracks'].append(track)
        if p_play_songs_to_add['tracks'] != None:
            p_add_id = plat_1.get_songs_id(p_play_songs_to_add)
            plat_1.add_songs(play_1, p_add_id)
        
        s_play_songs_to_add = {'tracks': []}
        for track in primeira_playlist['tracks']:
            for name in s_add:
                if is_equal(track['name'], name):
                    s_play_songs_to_add['tracks'].append(track)
        if s_play_songs_to_add["tracks"] != None:
            s_add_id = plat_2.get_songs_id(s_play_songs_to_add)
            plat_2.add_songs(play_2, s_add_id)

        # retornando html em caso de sucesso na sincronização
        success_html = """
        <div class="text-center space-y-4">
            <div class="text-2xl font-bold text-white mb-4">
                ✨ Sincronização Completa! ✨
            </div>
            <p class="text-white mb-6">
                As playlists '{}' e '{}' foram sincronizadas com sucesso!
            </p>
            <a href="/" 
            class="inline-block px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                Voltar
            </a>
        </div>
        """.format(
            play_1, play_2
        )
        return success_html
    except Exception as e:
        message = "Desculpe-nos, ocorreu um erro no final da sincronização. Avise o desenvolvedor e iremos trabalhar para arrumar!"
        print(e)
        return render_template("erro_swap.html", message=message)

@views.route("/baixar", methods=["GET", "POST"])
def baixar():
    if request.method == "GET":
        return render_template("baixar.html")
    step = request.args.get("step", type=int)
    if step == 1:
        plataforma = request.form.get("plataforma_baixar")
        session["entrada"] = plataforma
        plataform = get_platform(plataforma)
        playlists = plataform.get_playlists()

        return render_template_string("""
            <div class="mb-4">                         
            <label for="playlist" class="block text-sm font-medium text-gray-700">Escolha uma playlist do {{plataforma}}:</label>
            <select 

                id="playlist" 
                name="playlist"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                <option value="">Selecione uma playlist</option>
                {% for playlist in playlists %}
                <option value="{{playlist}}">{{playlist}}</option>
                {% endfor %}
            </select>
            </div>
        <button
        hx-post="/baixar?step=2"
        hx-include="#playlist"
        class="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
        Enviar
        </button>""", playlists=playlists, plataforma=plataforma)
    elif step == 2:
        playlist = request.form.get("playlist")
        session["baixar_playlist"] = playlist

        response = make_response("", 200)
        response.headers["HX-Redirect"] = url_for("views.download_template")
        return response

@views.route("/download_template", methods=["GET"])
def download_template():
    return render_template("download_template.html")

@views.route('/download', methods=['POST'])
def start_download():
    try:
        plataforma = session.get('entrada')
        if plataforma == "youtube":
            playlist_name = session.get('baixar_playlist')
            plat = get_platform(plataforma)
            plat.playlist_public(playlist_name)
            time.sleep(1)
            url = plat.get_playlist_url(playlist_name)
        else:
            playlist = session.get('baixar_playlist')
            plat = get_platform(plataforma)
            youtube = get_platform("youtube")
            plat_songs = plat.get_songs(playlist)
            songs_id = youtube.get_songs_id(plat_songs)
            playlist_name = playlist + "_baixar_yourplaylist"
            youtube.new_playlist(playlist_name,songs_id)
            time.sleep(2)
            youtube.playlist_public(playlist_name)
            time.sleep(2)
            url = youtube.get_playlist_url(playlist_name)
            session['baixar_playlist'] = playlist_name
        # Começar download em uma nova thread
        thread = threading.Thread(target=download_playlist, args=(url,))
        thread.start()
        
        return """
            <div class="text-center text-green-700 font-medium">
                Download iniciado! Acompanhe o progresso abaixo.
            </div>
        """
    except Exception as e:
        message = "Desculpe-nos, ocorreu um erro ao fazer o download. Avise o desenvolvedor e iremos trabalhar para arrumar!"
        return render_template("erro_swap.html", message=message)
progress_data = {}
def progress_hook(d):
    video_id = d['info_dict']['id']
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded_bytes = d.get('downloaded_bytes', 0)
        percent = downloaded_bytes / total_bytes * 100
        speed = d.get('speed')
        speed_str = f"{speed/1024/1024:.2f}MiB/s" if speed else "N/A"

        progress_data[video_id] = {
            'title': d['info_dict']['title'],
            'percent': f"{percent:.2f}%",
            'speed': speed_str,
            'eta':str(d.get('eta', 'Desconhecido')),
            'status': 'downloading'
        }
    elif d['status'] == 'finished':
        progress_data[video_id] = {
            'title': d['info_dict']['title'],
            'percent': '100%',
            'speed': '0 MiB/s',
            'eta': '0',
            'status': 'Completed'
        }

def download_playlist(url):
    """Fazendo download da playlist com yt-dlp"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'yourplaylist_downloads/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
        'noplaylist': False,  # Certifica que a playlist inteira é baixada
        # 'simulate': True #simulando downloads, sem salvar o arquivo, apenas para ambiente de teste
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@views.route('/progress', methods=['GET'])
def get_progress():
    return jsonify(progress_data)

@views.route('/download_completed', methods=['GET'])
def toque_final():
    plataforma = session.get('entrada')
    playlist = session.get('baixar_playlist')
    if plataforma == "youtube":
        plat = get_platform(plataforma)
        plat.playlist_private(playlist)
    else:
        plat = get_platform('youtube')
        plat.delete_playlist(playlist)
    return "", 204