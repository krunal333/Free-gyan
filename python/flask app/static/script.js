function movieTemplate(movie) {
  return `
  <div class="card card-list-style">
  <a class="link" href="${movie.link}" class=""first-hidden">
  <div class="card-content">
      <div class="col-xs-4 col-sm-3 image-column">
          <div class="image-style">
              <img ${movie.cover ? 'class="cover" src='+movie.cover : 'class="cover no_poster" src="no_poster.png"'} height="auto" width="100%">
            
          </div>
      </div>
      
      <div class="col-xs-8 vertical-box">
          <div class="author-info">
                  <div class="catagory">${movie.category}</div>
                  <p>
                      <span>
                          <b>${movie.name}</b><span class="size"> with ${movie.author_name} </span>
                      </span>
                  </p>
                  <div class="discription">
                  ${movie.course_description}
                  </div>
                  <div class="meta">
                      <span>${movie.time}</span>
                      <span class="meta-level">${movie.level}</span>
                      <span class="meta-views"> Views : ${movie.views}</span>
                  </div>
          </div>
      </div>
  </div>
  </a>
</div>

`
}


document.getElementById("records").innerHTML = `
${moviesData.map(movieTemplate).join("")}
`;





