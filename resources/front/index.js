import Vue from 'vue';
import $ from 'jquery';
import TableVacancies from './components/TableVacanciesComponent'
import '../assets/css/cosmetic.css';
import '../assets/css/materialize.min.css';
import '../assets/css/style.scss';

new Vue({
    el:"#index",
    data: {
        socket: null
    },
    components: {
        'table-vacancies': TableVacancies
    },
    mounted(){
        this.socket = new WebSocket("ws://localhost:8765");
        this.socket.onopen = function() {
            console.log("Соединение установлено.");
          };
          
        this.socket.onclose = function(event) {
          if (event.wasClean) {
            console.log('Соединение закрыто чисто');
          } else {
            console.log('Обрыв соединения'); // например, "убит" процесс сервера
          }
          console.log('Код: ' + event.code + ' причина: ' + event.reason);
        };
        
        this.socket.onmessage = function(event) {
          console.log("Получены данные " + event.data);
        };
        
        this.socket.onerror = function(error) {
          console.log("Ошибка " + error.message);
        };
        setTimeout(() => {
          this.socket.send("Привет");
        }, 2000)

    },

})
