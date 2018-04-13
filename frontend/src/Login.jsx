import React, {Component} from '../node_modules/react'

class Login extends Component{
    constructor(props){
        super(props)
        this.state = {
            username: '',
            password: ''
        }
        this.onClickHandler = this.onClickHandler.bind(this);
        this.onUsernameChange = this.onUsernameChange.bind(this);
        this.onPasswordChange = this.onPasswordChange.bind(this);
    }

    onClickHandler(){
        this.props.loginStart(
            this.state.username,
            this.state.password
        );
    }

    onUsernameChange(event){
        this.setState({
            username: event.target.value
        });
    }

    onPasswordChange(event){
        this.setState({
            password: event.target.value
        });
    }

    render(){
        return <div>
            <p>Please enter your username and password for {this.props.server}</p>
            <input 
                type="text" 
                value={this.state.username} 
                onChange={this.onUsernameChange}/>
            <input 
                type="password" 
                value={this.state.password} 
                onChange={this.onPasswordChange}/>
            <button onClick={this.onClickHandler}>></button>
        </div>
    }
}

export default Login