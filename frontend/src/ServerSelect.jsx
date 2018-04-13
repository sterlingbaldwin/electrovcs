import React, {Component} from '../node_modules/react'

class ServerSelect extends Component{
    constructor(props){
        super(props)
        this.state = {
            'address': this.props.default_server || 'localhost:8000'
        }
        this.onClickHandler = this.onClickHandler.bind(this);
        this.onInputChange = this.onInputChange.bind(this);
    }

    onClickHandler(){
        this.props.setServer(this.state.address);
    }

    onInputChange(event){
        this.setState({
            address: event.target.value
        });
    }

    render(){
        return(
            <div>
                <input 
                    value={this.state.address} 
                    onChange={this.onInputChange} 
                    type="text" />
                <button onClick={this.onClickHandler}>></button>
            </div>
        )
    }
}

export default ServerSelect
