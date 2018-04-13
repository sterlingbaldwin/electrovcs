import React, {Component} from '../node_modules/react'
import ServerSelect from './ServerSelect.jsx'
import Login from './Login.jsx'
import ScriptSelect from './ScriptSelect'


class App extends Component{
    constructor(props){
        super(props)
        this.state = {
            'default_server': 'localhost:8000',
            'server_address': '',
            'step': 0
        }
        this.onSetServer = this.onSetServer.bind(this);
        this.onLoginStart = this.onLoginStart.bind(this);
    }


    onSetServer(address){
        this.setState({
            server_address: address,
            step: 1
        }, () => {
            var url = 'http://' + this.state.server_address + '/django-pam/login/'
            fetch(url).then((res) => {
                
            })
        })
    }

    onLoginStart(username, password){
        var url = 'http://' + this.state.server_address + '/login/'
        fetch(url, {
            method: 'POST',
            credentials: "same-origin",
            body: JSON.stringify({
                'username': username,
                'password': password
            })
        }).then(() => {
            this.setState({step: 2});
        })
    }

    render(){
        var elem;
        if(this.state.step == 0){
            elem = (<ServerSelect 
                        default_server={this.state['default_server']}
                        setServer={this.onSetServer}/>)
        } else if (this.state.step == 1){
            elem = (<Login
                        server={this.state.server_address}
                        loginStart={this.onLoginStart}/>)
        } else if (this.state.step == 2)
            elem = ()
        
        return (
            <div>
                {elem}
            </div>
        )
    }

}

export default App