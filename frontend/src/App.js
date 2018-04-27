import React, {Component} from 'react';
import fetch from 'isomorphic-fetch';
import 'react-virtualized/styles.css'
//import rxFetch from 'rx-fetch';
import './App.css';


class App extends Component {
  constructor() {
    super();
    this.state = { url: '',
                  pname: '',
                  price: ''};
    this.onSubmit = this.handleSubmit.bind(this);
  }

    async handleSubmit(e) {
    //console.log(self.refs.link)
    e.preventDefault();
    var self = this;
    this.setState({url: this.refs.link.value})

    let response = await fetch('http://127.0.0.1:8000/getInfo', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin' : 'http://localhost:8000/getInfo',
        },
      body: JSON.stringify({
        url: this.refs.link.value
        })
      })
      let responseJson = await response.json();
      self.setState({ pname: responseJson.pname, price: responseJson.price })
      console.log(self.state.url);
      console.log(self.state.pname);
      console.log(self.state.price);
      // .then(function(response) {
      //   return response
      // }).then(function(body) {
      //   console.log(body);
    //});

//     let data1 = [];
//     Rx.DOM.ajax({
//                     url: 'http://127.0.0.1:8000/getInfo',
//                     responseType: 'json',
//                     method: 'POST',
//                     body: JSON.stringify({
//                          url: "https://www.amazon.in/WOW-Imagine-Premium-Brushed-Texture/dp/B077Y1MPMH/ref=br_asw_pdt-5?pf_rd_m=A1VBAL9TL5WCBF&pf_rd_s=&pf_rd_r=3MH8YN84SGDC356PB7Z6&pf_rd_t=36701&pf_rd_p=68c6c505-c771-4777-8e05-b1bf66e31f18&pf_rd_i=desktop"
//                        }),
//                 })
//                 .subscribe(
//                    data => {
//                         data.response.forEach(function(product) {
//                             //console.log(product);
//                             data1.push(product);
//                             //debugger;
//                         });
//                         this.setState({ users: data1 });
//                         //debugger;
//                     },
//                     err => {
//                         console.log(err);
//                     }
//                 );
  }
  render() {
    return (
      <div>
        <form onSubmit={this.onSubmit}>
          <label>Enter Url: </label>
          <input type="text" placeholder="URL here" ref="link"/>
          <input type="submit" />
        </form>
        <p>Product Name: {this.state.pname}</p>
        <p>Price: {this.state.price}</p>
      </div>
    );
  }
}

export default App;
