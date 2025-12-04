d3.csv("merged_clusters.csv", function(d) {
    return {
        cluster: d.cluster, //declare types and names
        len: +d.length,
        npl: +d.occurences_pl, 
        nen: +d.occurences_en,
        fpl: +d.frequency_pl,
        fen: +d.frequency_en,
        fttl: +d.total_frequency,//total frequency
        frel: +d.relative_frequency//relative frequency
    }
}).then(function(data) {


    //CLEVELAND DOT PLOT
    const svg = d3.select("#cl_dot_plot") //select svg object
    const tooltip = d3.select("#tooltip") //and select tooltips
    const axis = 75 //leave space for axes
    const hsize = 800 //height
    const wsize = 500 //length
    data.sort((a, b) => d3.ascending(a.frel, b.frel)) //sort by relative frequency

    filtered = data.filter(d=>d.fttl > 0.1)//starting value for frequency filter

    const x = d3.scaleLinear() //x values
        .domain([0,1])
        .range([axis,wsize-axis])

    const y = d3.scaleBand() //y values
        .domain(filtered.map(d=>d.cluster)) //make band for each
        .range([30, hsize-axis]) // flip y axis to start at bottom

    svg.selectAll("circle") //make circles for all points
        .data(filtered)
        .enter().append("circle")
        .attr("cx", d => x(d.frel))
        .attr("cy", d => y(d.cluster) + y.bandwidth()/2)
        .attr("r", 3) //radius must be large to avoid issues with tooltips
        .on("mouseover", (event, d) => {//when mouse is over dot
            tooltip.style("opacity",1)//make tooltip apparent
                .html(`Cluster: ${d.cluster}<br>Relative Frequency: ${d.frel}`) //show these stats
        }).on("mousemove", (event) => {
            tooltip.style("left", event.pageX + 10 + "px")
                    .style("top", event.pageY + "px")
        }).on("mouseout", () => tooltip.style("opacity",0))//make transparent when mouse moves

    svg.selectAll(".stem") //tracking lines
        .data(filtered)
        .join("line")
        .attr("class", "stem")
        .attr("x1", x(0))
        .attr("x2", d => x(d.frel))
        .attr("y1", d => y(d.cluster) + y.bandwidth()/2)
        .attr("y2", d => y(d.cluster) + y.bandwidth()/2)
        .attr("stroke", "grey")
        .attr("stroke-width", 1)
        .attr("stroke-opacity", 0.3)//keep light
    
    svg.append("g") //x axis
        .attr("class", "x-axis")
        .attr("transform", "translate(0, " + 740 + ")")
        .call(d3.axisBottom(x))

    svg.append("g") //y axis
        .attr("class", "y-axis")
        .attr("transform", "translate(" + 60 + ", 0)")
        .call(d3.axisLeft(y).tickPadding(0))

    svg.append("line")//center line
        .attr("x1",250)
        .attr("x2",250)
        .attr("y1",0)
        .attr("y2",725)
        .attr("stroke","black")
        .attr("stroke-opacity", 0.5)                    

    d3.select("#threshold").on("input", function () { //when slider moved, call update
        const value = +this.value //slider value
        d3.select("#threshold-value").text(value.toFixed(3))//fix text
        clevelandScope(value) //update plot              
    })

    function clevelandScope(threshold) {//called when desired frequency filter is changed

        const filtered = data.filter(d => d.fttl >= threshold) //update filter
        y.domain(filtered.map(d=>d.cluster)) //update clusters
        svg.select(".y-axis") //update y axis
            .call(d3.axisLeft(y).tickPadding(10))

        svg.selectAll(".stem") //update lines
            .data(filtered)
            .join("line")
            .attr("class", "stem")
            .attr("x1", x(0))
            .attr("x2", d => x(d.frel))
            .attr("y1", d => y(d.cluster) + y.bandwidth()/2)
            .attr("y2", d => y(d.cluster) + y.bandwidth()/2)
            .attr("stroke", "grey")
            .attr("stroke-width", 1)
            .attr("stroke-opacity", 0.3)//keep light
        
        const circles = svg.selectAll("circle")
            .data(filtered, d => d.cluster)

        circles.exit().remove() //remove old

        circles.enter() //add new
            .append("circle")
            .merge(circles)
            .attr("cx", d => x(d.frel))
            .attr("cy", d => y(d.cluster) + y.bandwidth()/2)
            .attr("r", 3)
            .on("mouseover", (event, d) => {//when mouse is over dot
                tooltip.style("opacity",1)//make tooltip apparent
                    .html(`Cluster: ${d.cluster}<br>Relative Frequency: ${d.frel}`) //show these stats
            }).on("mousemove", (event) => {
                tooltip.style("left", event.pageX + 10 + "px")
                        .style("top", event.pageY + "px")
            }).on("mouseout", () => tooltip.style("opacity",0))//make transparent when mouse moves
    }




    //SCATTERPLOT
    const svg2 = d3.select("#scatterplot") //plots are separate 
    const size2 = 800
    var zoom = 0.4 //zoom distance; changable
    var min_chars = 2 //min chars in cluster; changable
    filtered2 = data.filter(d=>d.fttl > 0.04) //use separate filtering

    const x2 = d3.scaleLinear() //x values
        .domain([0,zoom])
        .range([axis,size2-axis])

    const y2 = d3.scaleLinear() //y values
        .domain([0,zoom])
        .range([size2-axis,axis])

    svg2.selectAll("circle") //make circles for all points
        .data(filtered2)
        .enter().append("circle")
        .attr("cx", d => x2(d.fpl))
        .attr("cy", d => y2(d.fen))
        .attr("r", 3) //radius must be large to avoid issues with tooltips
        .on("mouseover", (event, d) => {//when mouse is over dot
            tooltip.style("opacity",1)//make tooltip apparent
                .html(`Cluster: ${d.cluster}<br>Polish Frequency: ${d.fpl}<br>English Frequency: ${d.fen}`) //show these stats
        }).on("mousemove", (event) => {
            tooltip.style("left", event.pageX + 10 + "px")
                    .style("top", event.pageY + "px")
        }).on("mouseout", () => tooltip.style("opacity",0))//make transparent when mouse moves

    svg2.append("g") //x axis
        .attr("class", "x-axis")
        .attr("transform", "translate(0, " + 740 + ")")
        .call(d3.axisBottom(x2))

    svg2.append("g") //y axis
        .attr("class", "y-axis")
        .attr("transform", "translate(" + 60 + ", 0)")
        .call(d3.axisLeft(y2))

    svg2.append("line")//dividing line
        .attr("x1",75)
        .attr("x2",600)
        .attr("y1",725)
        .attr("y2",200)
        .attr("stroke","black")
        .attr("stroke-opacity", 0.3)  
    
    svg2.append("line")//legend line
        .attr("x1",600)
        .attr("x2",600)
        .attr("y1",75)
        .attr("y2",200)
        .attr("stroke","black")
        .attr("stroke-opacity", 0.5)  

    svg2.append("line")//legend line
        .attr("x1",725)
        .attr("x2",600)
        .attr("y1",200)
        .attr("y2",200)
        .attr("stroke","black")
        .attr("stroke-opacity", 0.5)
    
    const colors = ["#ae282c", "#d47264", "#f6d6c2", "#8ec1da", "#2066a8","#7e4794"]
    var colorSet = d3.scaleQuantile() //color set
        .domain([2,3,4,5,6,7])
        .range(colors)

    svg2.selectAll("circle").attr("fill", d => colorSet(d.len))//colors start on
    
    //create legend
    svg2.append("text").attr("x",615).attr("y",90).text("# Sounds in Cluster").style("font-size", "14px")    
    for (let i = 0; i < 6; i++) {
        svg2.append("rect").attr("x",615).attr("y",106 + (15*i)).attr("r", 4)
            .style("fill", colors[i]).attr("width",8).attr("height",8)
        svg2.append("text").attr("x",635).attr("y",114 + (15*i)).text(i+2).style("font-size", "14px")
    }
    

    const checkbox = d3.select("#coloring")//checkbox object
    
    checkbox.on("change", function() {//switch between color and no color
        if (this.checked) {
            svg2.selectAll("circle").attr("fill", d => colorSet(d.len))
        } else {
            d3.selectAll("circle").attr("fill", "black")
        }
    })
    
    d3.selectAll('input[name="choice"]').on("change", function() {
        if (this.checked) {
            zoom = this.value
            updatePlot() //when zoom is changed, call this
        }
    })

    d3.selectAll('input[name="min"]').on("change", function() {
        if (this.checked) {
            min_chars = this.value
            updatePlot() //when min chars is changed, call this
        }
    })

    function updatePlot() {
        
        //update data
        if (zoom == 0.001) {
            filtered2 = data.filter(d=>d.fpl < zoom && d.fen < zoom && d.len >= min_chars)
        } else {//dont show lower extremes when zoomed out; very crowded
            filtered2 = data.filter(d=>d.fttl > (0.1 * zoom) && d.fpl < zoom && d.fen < zoom
                                     && d.len >= min_chars)
        }

        x2.domain([0,zoom])//update domains
        y2.domain([0,zoom])

        svg2.select(".x-axis") //update x axis
            .call(d3.axisBottom(x2).tickPadding(10))
        svg2.select(".y-axis") //update y axis
            .call(d3.axisLeft(y2).tickPadding(10))

        const circles2 = svg2.selectAll("circle")
            .data(filtered2)

        circles2.exit().remove() //remove old

        circles2.enter() //add new
            .append("circle")
            .merge(circles2)
            .attr("cx", d => x2(d.fpl))
            .attr("cy", d => y2(d.fen))
            .attr("r", 3)
            .on("mouseover", (event, d) => {//when mouse is over dot
                tooltip.style("opacity",1)//make tooltip apparent
                    .html(`Cluster: ${d.cluster}<br>Polish Frequency: ${d.fpl}<br>English Frequency: ${d.fen}`) //show these stats
            }).on("mousemove", (event) => {
                tooltip.style("left", event.pageX + 10 + "px")
                        .style("top", event.pageY + "px")
            }).on("mouseout", () => tooltip.style("opacity",0))//make transparent when mouse moves
        
        if (zoom == 0.001) { //we get to grid level, so jittering is necessary
            svg2.selectAll("circle")
                .attr("cx", d => x2(d.fpl) + (30* (Math.random()-0.5)))
                .attr("cy", d => y2(d.fen) + (30* (Math.random()-0.5)))
        }

        if (checkbox.property("checked") == true) {//recolor everything same way
            svg2.selectAll("circle").attr("fill", d => colorSet(d.len))
        } else {
            d3.selectAll("circle").attr("fill", "black")
        }


    }

    //TREEPLOT
    size3 = 800//weird bounding for radial trees so must adjust
    const svg3 = d3.select("#tree_plot").attr("viewBox", [-size3/2, -size3/2, size3, size3])
    const radius = 400


    //turn cluster strings into a tree of nodes and children
    function buildUnicodeTreeWithAllParents(data) {
        const segmenter = new Intl.Segmenter(undefined, { granularity: "grapheme" }) //allows ipa
        function graphemes(str) { return Array.from(segmenter.segment(str), s => s.segment) }

        const root = { name: "root", children: [] } //root node
        const lookup = { root: root } //dict which carries each node and info about it

        data.forEach(row => { //for each cluster
            const chars = graphemes(row.cluster) //turn cluster to array of chars
            for (let i = 1; i <= chars.length; i++) { //iterate through chars
                const key = chars.slice(0, i).join("") //key = first i letters
                if (!lookup[key]) { //if key doesnt yet have dict entry
                    const parentKey = i == 1 ? "root" : chars.slice(0, i - 1).join("")//parentkey = key-1char
                    const node = { name: key, children: []}//make node for key
                    lookup[key] = node//add dict entry with key
                    lookup[parentKey].children.push(node) //add key as child to parent
                    
                }
            }
            
        })

        return root //finally, return root (and all other keys with it)
    }

    // convert polar to normal coordinates
    function polarToCartesian(angle, r) {
        return [r * Math.cos(angle - Math.PI/2), r * Math.sin(angle - Math.PI/2)]
    }

    const colorSet2 = d3.scaleSequential()//red to blue gradient
        .domain([0,1])
        .interpolator(d3.interpolateRgb("red","blue"))

    const treeLayout = d3.tree().size([2*Math.PI, radius-100])//tree dimensions (polar)
    const treeData = buildUnicodeTreeWithAllParents(data)//build tree structure
    var currentRoot = treeData //track what the current root of the tree is
    var maxDepth = 0

    function render(rootData) {//display tree
        svg3.selectAll("*").remove() //clear entire plot
        const root = d3.hierarchy(rootData) //turn tree into d3 object


        if (root.children?.length > 12) {maxDepth = 0}//if too many children, cannot handle so many layers
        else {maxDepth = 2}

        root.each(d => {
            if (d.depth > maxDepth) {
                d._children = d.children// store children that are too deep to show
                d.children = null// hide them from this render
            }
        })


        treeLayout(root) //attach object to tree layout

        //connecting lines
        svg3.append("g")
            .selectAll("line")
            .data(root.descendants().slice(1))//attach all immediate children and their parent
            .join("line")
            .attr("x1", d => polarToCartesian(d.parent.x, d.parent.y)[0])
            .attr("y1", d => polarToCartesian(d.parent.x, d.parent.y)[1])
            .attr("x2", d => polarToCartesian(d.x, d.y)[0])
            .attr("y2", d => polarToCartesian(d.x, d.y)[1])
            .attr("stroke", "grey")

        //nodes
        const nodes = svg3.append("g")
            .selectAll("g")
            .data(root.descendants())//attach node to each tree node
            .join("g")
            .attr("transform", d => {
                const [x, y] = polarToCartesian(d.x, d.y)
                return `translate(${x},${y})`
            })

        nodes.append("circle")//put a circle on each node
            .attr("r", 4)
            .on("click", (event, d) => {//when clicked
                event.stopPropagation() //prevent additional clicks

                
                if (d.data == currentRoot) { //if clicked root, reset tree
                    render(treeData)
                } else {//else reroot at clicked node
                    currentRoot = d.data
                    render(currentRoot)
                }


            })

        nodes.selectAll("circle")
            .attr("fill", d => {
                const row = data.find(r => r.cluster == d.data.name)//match names to use csv row
                if (!row) return "black" //for single letters which don't have a row
                return colorSet2(row.frel) //color by relative frequency from that row
            })

        nodes.append("text")
            .attr("dy", -8) //put cluster text 8 px above the node
            .text(d => d.data.name)

        //legend
        svg3.append("rect").attr("x",300).attr("y",-300).attr("r", 4)
            .style("fill", "red").attr("width",8).attr("height",8)
        svg3.append("text").attr("x",320).attr("y",-291).text("More English").style("font-size", "14px")

        svg3.append("rect").attr("x",300).attr("y",-280).attr("r", 4)
            .style("fill", "blue").attr("width",8).attr("height",8)
        svg3.append("text").attr("x",320).attr("y",-271).text("More Polish").style("font-size", "14px")
    }
    

    render(treeData) //render tree the first time
})