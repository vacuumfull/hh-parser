import Vue from 'vue';
import HelperMixin from '../mixins/HelperMixin'; 
import template from '../../tmp/components/table-vacancies.html';

const TableVacancies = Vue.extend({
    template,
    mixins: [HelperMixin],
    data(){
        return {
            vacancies: [],
            limit: 0,
            showTable:  false,
        }
    },
    mounted(){
        this.getVacancies()
    },
    methods: {
        getVacancies(){
            let self = this,
                uri = `/vacancy/api/`
            fetch(uri, {method: 'GET'})
                .then(response => {
                    return response.json()
                })
                .then(vacancies => {
                    self.vacancies = vacancies;
                    if (self.vacancies.length > 0) self.showTable = true;
                })
                .catch(error => {
                    console.error(error)
                }
            )
        },
        link(id){
            window.location.href = `${window.location.origin}/vacancy/${id}`
        },
        remove(){
            let self = this,
                uri = `/vacancy/remove/`
                fetch(uri, {method: 'GET'})
                    .then(response => {
                        return response.json()
                    })
                    .then(info => {
                        console.log(info)
                        self.getVacancies()
                        self.showTable = false;
                    })
                    .catch(error => {
                        console.error(error)
                    }
                )
        },
        cycleStart(){
            let self = this;
            setInterval(() => {
                self.getVacancies()
            }, 10000)
        },
        start(){
            let self = this,
                uri = `/parser/start/${self.limit}`;
                self.cycleStart();
                fetch(uri, {method: 'GET'})
                    .then(response => {
                        return response.json()
                    })
                    .then(info => {
                        console.log(info)
                    })
                    .catch(error => {
                        console.error(error)
                    })
            }
    }
})

export default TableVacancies;