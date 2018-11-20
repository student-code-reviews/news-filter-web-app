class NewsOptions extends React.Component {
    render() {
    return(

<ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
  <li class="nav-item">
    <a class="nav-link active" id="pills-home-tab" data-toggle="pill" href="#pills-home" role="tab">Home</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" id="pills-profile-tab" data-toggle="pill" href="#pills-profile" role="tab">Profile</a>
  </li>
  <form action="/hello">
    <li class="nav-item">
      <button class="nav-link" id="pills-contact-tab" data-toggle="pill" role="tab" type="submit">Contact</button>
    </li>
  </form>
</ul>



      );
  }
}

ReactDOM.render(<NewsOptions />, document.querySelector(" #root"));
