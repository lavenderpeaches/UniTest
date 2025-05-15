const app = Vue.createApp({
    data() {
        return{
            enteredName: '',
        }
    },
    method: {
        testName($event){
            this.enteredName = $event.target.value;
        }
    }
})

app.mount('#app');