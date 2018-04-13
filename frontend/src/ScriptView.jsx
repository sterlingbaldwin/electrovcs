import React, {Component} from '../node_modules/react'

class ScriptView extends Component{
    constructor(props){
        super(props)
        this.state = {
            'server': this.props.server_address || 'localhost:8000',
            'contents': '',
            'img_path': '',
            'script_path': '',
            'output': '',
            'error': '',
        }
        this.handleChange = this.handleChange.bind(this);
        this.handleSave = this.handleSave.bind(this);
        this.onPlot = this.onPlot.bind(this);
    }

    componentDidMount(){
        var url = 'http://' + this.state.server + '/viz/get/'
        fetch(url, {
            method: 'POST',
            credentials: "include",
            headers: {
                Accept: 'application/json'
            },
            body: JSON.stringify({
                'username': this.props.username,
                'password': this.props.password,
                'method': 'GET',
                'script': this.props.script
            })
        }).then((res) => {
            res.json().then(json => {
                console.log(json);
                if(json.found){
                    this.setState({
                        'contents': json.contents,
                        'img_path': json.img_path,
                        'script_path': json.script_path
                    })
                }
            });
        }).catch((res) => {
            console.log('get vis list error');
            console.log(res);
        });
    }

    handleChange(event){
        this.setState({
            'contents': event.target.value
        })
    }

    handleSave(){
        var url = 'http://' + this.state.server + '/viz/save/'
        fetch(url, {
            method: 'POST',
            credentials: "include",
            headers: {
                Accept: 'application/json'
            },
            body: JSON.stringify({
                'username': this.props.username,
                'password': this.props.password,
                'script': this.props.script,
                'contents': this.state.contents
            })
        }).then((res) => {
            console.log('save should have worked')
        }).catch((res) => {
            console.log('save failed');
            console.log(res);
        });
    }

    onPlot(event){
        var url = 'http://' + this.props.server + '/viz/run/'
        console.log('plotting', event.target.value)
        fetch(url, {
            method: 'POST',
            credentials: "same-origin",
            timeout: 0,
            body: JSON.stringify({
                'username': this.props.username,
                'password': this.props.password,
                'script': event.target.value
            })
        }).then((res) => {
            res.json().then(json => {
                console.log(json);
                this.setState({
                    'img_path': json.img_path,
                    'output': json.out,
                    'error': json.err
                });
            })
        }).catch((res) => {
            this.setState({step: 2});
            console.log('plot error');
            console.log(res);
        });
    }

    render(){
        var elem;
        if(this.state.img_path){
            elem = (
                <img src={this.state.img_path} alt=""/>
            )
        } else {
            elem = (<br/>)
        }
        var elem2;
        if(this.state.output.length > 0 || this.state.error.length > 0){
            elem2 = (
                <div>
                    <p>Output:</p>
                    <p>{this.state.output}</p>
                    <p>Error:</p>
                    <p>{this.state.error}</p>
                </div>
            )
        } else {
            elem2 = (<br/>)
        }
        return (
            <div>
                <button onClick={this.props.back}>back</button>
                {elem}
                {elem2}
                <textarea 
                    cols="100"
                    rows={this.state.contents.split(/\r\n|\r|\n/).length} 
                    value={this.state.contents}
                    onChange={this.handleChange}>
                </textarea>
                <button onClick={this.handleSave}>save</button>
                <button onClick={this.onPlot} value={this.state.script_path}>run</button>
            </div>
        )
    }
}

export default ScriptView