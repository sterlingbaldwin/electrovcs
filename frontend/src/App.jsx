import React, {Component} from '../node_modules/react'
import ServerSelect from './ServerSelect.jsx'
import Login from './Login.jsx'
import ScriptSelect from './ScriptSelect.jsx'
import ScriptView from './ScriptView.jsx'


class App extends Component{
    constructor(props){
        super(props)
        this.state = {
            'default_server': 'localhost:8000',
            'server_address': '',
            'step': 0,
            'selected_script': '',
            'username': '',
            'password': ''
        }
        this.onSetServer = this.onSetServer.bind(this);
        this.onLoginStart = this.onLoginStart.bind(this);
        this.onSelectScript = this.onSelectScript.bind(this);
        this.onScriptViewBack = this.onScriptViewBack.bind(this);
    }

    onSelectScript(event){
        this.setState({
            'selected_script': event.target.value,
            'step': 3
        });
    }

    onScriptViewBack(event){
        this.setState({
            'step': 2
        })
    }


    onSetServer(address){
        this.setState({
            server_address: address,
            step: 1
        });
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
        }).then((res) => {
            this.setState({
                'step': 2,
                'username': username,
                'password': password});
        }).catch((res) => {
            this.setState({step: 1});
            console.log('login error');
            console.log(res);
        });
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
        } else if (this.state.step == 2){
            elem = (<ScriptSelect
                        server={this.state.server_address}
                        username={this.state.username}
                        password={this.state.password}
                        scriptSelect={this.onSelectScript}/>)
        } else if (this.state.step == 3){
            elem = (<ScriptView
                        server={this.state.server_address}
                        username={this.state.username}
                        password={this.state.password}
                        script={this.state.selected_script}
                        back={this.onScriptViewBack}/>)
        }
        
        return (
            <div>
                {elem}
            </div>
        )
    }

}

export default App