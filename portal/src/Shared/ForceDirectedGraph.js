




const forceDirectedGraphSketch = () => {

    return (p) => {

        p.preload = () => {
           
        }   
        p.setup = () => {
            p.createCanvas(round(windowWidth * 0.97), round(windowHeight * 0.97));
            p.frameRate(30);
            p.textFont("MS Gothic");
            pan_x = width / 2;
            pan_y = height / 2;
            for (let i = 0; i < database.elements.nodes.length; i++) {
              var node = database.elements.nodes[i];
              let x = p.random(-width/2, width/2)
              let y = p.random(-height/2, height/2)
              if (node.data.appeared) {
                node = new Node(p,p.createVector(x, y), node.data);
                nodes.push(node);
              }
            }
            draggedNode = nodes[0];
            for (let i = 0; i < database.elements.edges.length; i++) {
              var edge = database.elements.edges[i];
              var src = nodes.find((node) => node.data.name == edge.data.source);
              var dst = nodes.find((node) => node.data.name == edge.data.target);
              if (src && dst) {
                edges.push(new Edge(p,src, dst, edge.data));
              }
            }
            nodes.forEach((node) => {
              node.data["out_degree"] = edges.filter((edge) => edge.data.source == node.data.name).length;
              node.data["in_degree"] = edges.filter((edge) => edge.data.target == node.data.name).length;
              node.data["degree"] = node.data["in_degree"] + node.data["out_degree"];
            });
        };
        p.draw = () => {
            p.textAlign(CENTER, CENTER);
            p.translate(pan_x, pan_y);
            p.scale(zoom);
            
            p.background(BG_COLOR);
            p.applyForces(nodes)
            edges.forEach(edge => {
              edge.draw();
            })
            nodes.forEach(node => {
              node.draw();
              node.update();
            })
            edges.forEach(edge => {
              edge.drawText();
            })
            if (is_dragging_node) {
              let mousePos = p.createVector(mouseX - pan_x, mouseY - pan_y)
              draggedNode.pos.lerp(mousePos, lerpValue)
              if (lerpValue < 0.95) {
                  lerpValue += 0.02;
              }
            }
        };
    };
    
}


class Node {
    constructor(p, pos, data) {
      this.pos = pos;
      this.force = this.p.createVector(0, 0);
      this.data = data;
      this.updateSize();
      this.p = p;
    }
      
    updateSize() {
      this.size = (this.data.out_degree + 2) * 8;
      this.mass = (2 * PI * this.size) * 0.005;
    }
  
    update() {
      this.updateSize();
      var force = this.force.copy();
      var vel = force.copy().div(this.mass);
      this.pos.add(vel);
    }
  
    draw() {
      this.p.noStroke();
      this.p.fill(NODE_COLOR);
      if (this.isDragged()) {
        this.p.fill(NODE_DRAGGED_COLOR)
      } else if (this.isHovered()) {
        this.p.fill(NODE_HOVERED_COLOR)
      }
      this.p.ellipse(this.pos.x, this.pos.y, this.size, this.size);
      this.p.fill("black");
      var label_size = this.size;
      if (label_size < 50) {
        this.p.text(this.data.name, this.pos.x, this.pos.y);
      } else {
        this.p.text(this.data.name, this.pos.x - label_size / 2, this.pos.y - label_size / 2, label_size, label_size);
      }
    }
    
    isHovered() {
      return this.p.dist(
        (mouseX - pan_x) / zoom, 
        (mouseY - pan_y) / zoom,
        this.pos.x,
        this.pos.y
      ) < this.size / 2;
    }
    
    isDragged() {
      return draggedNode == this && is_dragging_node;
    }
    
    isVisible() {
      var global_pos_x = this.pos.x * zoom + pan_x;
      var global_pos_y = this.pos.y * zoom + pan_y;
      return global_pos_x > 0 && global_pos_x <= width && global_pos_y > 0 && global_pos_y <= height;
    }
  }
  
  class Edge {
    constructor(p, src, dst, data) {
      this.src = src;
      this.dst = dst;
      this.data = data;
      this.p = p;
    }
    
    draw() {
      var node1 = this.src;
      var node2 = this.dst;
      var diff = this.p.sqrt((node1.pos.x - node2.pos.x) * (node1.pos.x - node2.pos.x) + (node1.pos.y - node2.pos.y) * (node1.pos.y - node2.pos.y));
      var a = this.p.atan2(node2.pos.y - node1.pos.y, node2.pos.x - node1.pos.x);
      
      // if (!(node1.isVisible() || node2.isVisible())) return;
      
      var is_highlighted = (this.src.isHovered() || this.dst.isHovered() || this.src.isDragged() || this.dst.isDragged() || this.isHovered());
      
      this.p.push();
      this.p.fill(0);
      this.p.translate(node1.pos.x, node1.pos.y);
      var selected_color = "black";
      if (this.data.kind == "battle") {
        selected_color = EDGE_BATTLE_COLOR;
      } else if (this.data.kind == "mention") {
        selected_color = EDGE_MENTION_COLOR;
      } else if (this.data.kind == "cameo") {
        selected_color = EDGE_CAMEO_COLOR;
      }
      this.p.stroke(selected_color);
      this.p.fill(selected_color);
      if (is_highlighted) {
        this.p.strokeWeight(3);
      }
      
      this.p.push();
      this.p.rotate(a);
      this.p.triangle(diff - node2.size * 0.5, 0, diff - node2.size * 0.5 - 10, 5, diff - node2.size * 0.5 - 10, -5);
      this.p.line(0, 0, diff, 0);
      this.p.pop();
      this.p.pop();
    }
    
    drawText() {
      var node1 = this.src;
      var node2 = this.dst;
      var diff = this.p.sqrt((node1.pos.x - node2.pos.x) * (node1.pos.x - node2.pos.x) + (node1.pos.y - node2.pos.y) * (node1.pos.y - node2.pos.y));
      var a = this.p.atan2(node2.pos.y - node1.pos.y, node2.pos.x - node1.pos.x);
      
      // if (!(node1.isVisible() || node2.isVisible())) return;
      
      var is_highlighted = (this.src.isHovered() || this.dst.isHovered() || this.src.isDragged() || this.dst.isDragged() || this.isHovered());
      
      this.p.push();
      this.p.translate(node1.pos.x, node1.pos.y);
      var selected_color = "black";
      if (this.data.kind == "battle") {
        selected_color = EDGE_BATTLE_COLOR;
      } else if (this.data.kind == "mention") {
        selected_color = EDGE_MENTION_COLOR;
      } else if (this.data.kind == "cameo") {
        selected_color = EDGE_CAMEO_COLOR;
      }
      this.p.fill(selected_color);
      
      if (is_highlighted) {
        if (this.data.kind == "battle") {
          this.p.fill(EDGE_BATTLE_LABEL_COLOR);
        } else if (this.data.kind == "mention") {
          this.p.fill(EDGE_MENTION_LABEL_COLOR);
        } else if (this.data.kind == "cameo") {
          this.p.fill(EDGE_CAMEO_LABEL_COLOR);
        }
        // strokeWeight(1);
        this.p.translate(cos(a) * diff / 2, sin(a) * diff / 2);
        this.p.textAlign(LEFT, CENTER);
        // stroke('black');
        this.p.text(this.data.label, -100, 0, 200)
      }
      this.p.pop();
    }
    
    isHovered() {
      var x0 = (mouseX - pan_x) / zoom;
      var y0 = (mouseY - pan_y) / zoom;
      var x1 = this.src.pos.x, y1 = this.src.pos.y;
      var x2 = this.dst.pos.x, y2 = this.dst.pos.y;
      
      if (this.p.dist(x0, y0, x1, y1) + this.p.dist(x0, y0, x2, y2) >= 1.1 * this.p.dist(x1, y1, x2, y2)) {
        return false;
      }
      
      var dist_line = this.p.abs((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1)) / this.p.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
      return dist_line < 10;
    }
}


export { forceDirectedGraphSketch };