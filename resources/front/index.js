import Vue from 'vue';
import $ from 'jquery';
import TableVacancies from './components/TableVacanciesComponent'
import '../assets/css/cosmetic.css';
import '../assets/css/materialize.min.css';
import '../assets/css/style.scss';

new Vue({
    el:"#index",
    components: {
        'table-vacancies': TableVacancies
    },
})
