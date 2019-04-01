function search() {
        let input, filter, projects, project_title, div, current_div;
        input = document.getElementById("search_projects");
        filter = input.value.toUpperCase();
        projects = document.getElementsByClassName('homepage-card-container');
        div = document.getElementsByClassName('search-project');

        for(i = 0; i<projects.length; i++) {
            current_div = div[i];
            project_title = current_div.innerHTML;
            if(project_title.toUpperCase().indexOf(filter) > -1) {
                projects[i].style.display = "";
            }
            else{
                projects[i].style.display = "none";
            }
        }
};