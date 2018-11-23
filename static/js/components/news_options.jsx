
class NewsOptions extends React.Component {
      getUser = () => {
        fetch('/user.json')
          .then(response => response.json())
          .then(data => {
            const user_id = data.user_id
            window.location(url)
          });
        }

    render() {



    return(
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <form action="/filtered-news/${ user_id }">
            <button onClick={this.getUser} className="btn btn-info" name = "option" value="world">World</button>
        </form>

        <form action="/hello">
            <button className="btn btn-info" type="submit">Politics</button>
        </form>
        <form action="/hello">
            <button className="btn btn-info" type="submit">Technology</button>
        </form>
        <form action="/hello">
            <button className="btn btn-info" type="submit">Sports</button>
        </form>
        <form action="/hello">
            <button className="btn btn-info" type="submit">Entertainment</button>
        </form>
      </nav>

      );
  }
}


ReactDOM.render(<NewsOptions />, document.querySelector("div#root"));


