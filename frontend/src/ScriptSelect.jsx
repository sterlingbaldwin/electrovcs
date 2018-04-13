import React, {Component} from '../node_modules/react'

class ScriptSelect extends Component{
    constructor(props){
        super(props)
        this.state = {
            'server': this.props.server_address || 'localhost:8000',
            'scripts': [],
            'new_script_name': ''
        }
        this.onNewScript = this.onNewScript.bind(this);
        this.onInputChange = this.onInputChange.bind(this);
    }

    componentDidMount(){
        var url = 'http://' + this.state.server + '/viz/list/'
        fetch(url, {
            method: 'POST',
            credentials: "include",
            headers: {
                Accept: 'application/json'
            },
            body: JSON.stringify({
                'username': this.props.username,
                'password': this.props.password,
                'method': 'GET'
            })
        }).then((res) => {
            res.json().then(json => {
                console.log(json);
                this.setState({
                    'scripts': json
                })
            });
        }).catch((res) => {
            console.log('get vis list error');
            console.log(res);
        });
    }

    onNewScript(){
        var url = 'http://' + this.state.server + '/viz/list/'
        fetch(url, {
            method: 'POST',
            credentials: "include",
            headers: {
                Accept: 'application/json'
            },
            body: JSON.stringify({
                'username': this.props.username,
                'password': this.props.password,
                'method': 'POST',
                'name': this.state.new_script_name
            })
        }).then((res) => {
            var scripts = this.state.scripts
            scripts.push(this.state.new_script_name);
            this.setState({
                'scripts': scripts
            })
        }).catch((res) => {
            console.log('new viz script error');
            console.log(res);
        });
    }

    onInputChange(event){
        this.setState({
            new_script_name: event.target.value
        });
    }

    render(){
        return (
            <div>
                <div>
                    <input 
                        type="text" 
                        value={this.state.new_script_name}
                        onChange={this.onInputChange}/>
                    <button onClick={this.onNewScript}>
                        New Script
                    </button>
                </div>
                
                {this.state.scripts.map((script, i) => {
                    return (
                        <div>
                            <button 
                                onClick={this.props.scriptSelect}
                                value={script}>
                                {script}
                            </button>
                        </div>
                    )
                })}
            </div>
        )
    }
}

export default ScriptSelect