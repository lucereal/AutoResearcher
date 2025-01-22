import { database } from "../data/storyGraphData.js";


let BG_COLOR = "#f0eceb";
let NODE_COLOR = "#ff7a7a";
let NODE_HOVERED_COLOR = "#b66";
let NODE_DRAGGED_COLOR = "#a44";
let EDGE_BATTLE_COLOR = "#527aff";
let EDGE_BATTLE_LABEL_COLOR = "#3750a6";
let EDGE_MENTION_COLOR = "#39bd4c";
let EDGE_MENTION_LABEL_COLOR = "#247d31";
let EDGE_CAMEO_COLOR = "#d991ff";
let EDGE_CAMEO_LABEL_COLOR = "#935db0";
let IS_FOCUSED_ON_CANVAS = true;

let gravityConstant = 0.3;
let forceConstant = 4000;

let nodes = [];
let edges = [];
let lerpValue = 0.2;
let draggedNode;
let draggedNodeMag;
let is_dragging_node = false;
let last_mouse_pos = null;

let zoom = 0.5, pan_x = 0, pan_y = 0;

const storyGraphSketch = () => {

    const applyForces = (nodes) => {
        // apply force towards centre
        nodes.forEach((node) => {
          let gravity = node.pos.copy().mult(-1).mult(gravityConstant);
          node.force = gravity;
        })
      
        // apply repulsive force between nodes
        for (let i = 0; i < nodes.length; i++) {
          for (let j = i + 1; j < nodes.length; j++) {
            let pos = nodes[i].pos;
            let dir = nodes[j].pos.copy().sub(pos);
            let force = dir.div(dir.mag() * dir.mag());
            force.mult(forceConstant);
            nodes[i].force.add(force.copy().mult(-1));
            nodes[j].force.add(force);
          }
        }
      
        // apply forces applied by connections
        edges.forEach(edge => {
          let node1 = edge.src;
          let node2 = edge.dst;
          // let maxDis = edge[2];
          let dis = node1.pos.copy().sub(node2.pos);
          // diff = max(0.1, dis.mag() - maxDis);
          // diff = dis.mag() - maxDis;
          dis = dis.mult(0.1);
          node1.force.sub(dis);
          node2.force.add(dis);
        })
      }
    

    let pf = (p) => {
        const mouseClicked = () => {
            if (!IS_FOCUSED_ON_CANVAS) return;
            if (is_dragging_node) {
              is_dragging_node = false
              lerpValue = 0.2
            } else {
              nodes.forEach((node) => {
                if (node.isHovered()) {
                  is_dragging_node = true;
                  draggedNode = node;
                  return;
                }
              })
            }
          }
    
        const mouseReleased = () => {
            last_mouse_pos = null;
        }
    
        const mouseDragged = () => {
            if (!IS_FOCUSED_ON_CANVAS) return;
            if (is_dragging_node) return;
            
            if (last_mouse_pos) {
                var current_mouse_pos = p.createVector(p.mouseX, p.mouseY);
                pan_x += current_mouse_pos.x - last_mouse_pos.x;
                pan_y += current_mouse_pos.y - last_mouse_pos.y;
            }
            
            last_mouse_pos = p.createVector(p.mouseX, p.mouseY);
        }
        const keyPressed = () => {
            if (p.key == '-') {
                applyScale(0.95);
            } else if (p.key == '+') {
                applyScale(1.05);
            } 
        }
        
        const applyScale = (s) => {
          console.log("applying scale")
          if (!IS_FOCUSED_ON_CANVAS) return;
          if ((zoom > 1.5 && s > 1) || (zoom < 0.2 && s < 1)) {
              return;
          }
          zoom = zoom * s;
          pan_x -= (p.mouseX - pan_x) * (s - 1);
          pan_y -= (p.mouseY - pan_y) * (s - 1);
        }


        const handleWheel = (e) => {
          applyScale(e.deltaY > 0 ? 0.95 : 1.05);
        };

        p.mouseClicked = mouseClicked;
        p.mouseReleased = mouseReleased;
        p.mouseDragged = mouseDragged;
        p.keyPressed = keyPressed;
        p.preload = () => {
           
        }   
        p.setup = () => {
          console.log("forceDirectedGraphSketch setup")

          console.log("nodes length: " + nodes.length);
          console.log("edges length: " + edges.length);
          nodes = [];
          edges = [];
          
          p.createCanvas(p.round(window.innerWidth * 0.97), p.round(window.innerHeight * 0.97));
          p.frameRate(30);
          p.textFont("MS Gothic");
          pan_x = p.width / 2;
          pan_y = p.height / 2;
          for (let i = 0; i < database.elements.nodes.length; i++) {
            var node = database.elements.nodes[i];
            let x = p.random(-p.width/2, p.width/2)
            let y = p.random(-p.height/2, p.height/2)
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

          window.addEventListener("wheel", handleWheel);

        };
        p.draw = () => {
          
            p.textAlign(p.CENTER, p.CENTER);
            p.translate(pan_x, pan_y);
            p.scale(zoom);
            
            p.background(BG_COLOR);
            //applyForces(nodes)
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
              let mousePos = p.createVector(p.mouseX - pan_x, p.mouseY - pan_y)
              draggedNode.pos.lerp(mousePos, lerpValue)
              if (lerpValue < 0.95) {
                  lerpValue += 0.02;
              }
            }
        };
        
        p.remove = () => {
          console.log("forceDirectedGraphSketch remove")
          nodes = [];
          edges = [];
          window.removeEventListener("wheel", handleWheel);

        }
    };
    return pf;
}


class Node {
    constructor(p, pos, data) {
      this.pos = pos;
      this.force = p.createVector(0, 0);
      this.data = data;
      this.updateSize();
      this.p = p;
    }
      
    updateSize() {
      this.size = (this.data.out_degree + 2) * 8;
      this.mass = (2 * 3.1416 * this.size) * 0.005;
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
        (this.p.mouseX - pan_x) / zoom, 
        (this.p.mouseY - pan_y) / zoom,
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
      return global_pos_x > 0 && global_pos_x <= this.p.width && global_pos_y > 0 && global_pos_y <= this.p.height;
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
        this.p.translate(this.p.cos(a) * diff / 2, this.p.sin(a) * diff / 2);
        this.p.textAlign(this.p.LEFT, this.p.CENTER);
        // stroke('black');
        this.p.text(this.data.label, -100, 0, 200)
      }
      this.p.pop();
    }
    
    isHovered() {
      var x0 = (this.p.mouseX - pan_x) / zoom;
      var y0 = (this.p.mouseY - pan_y) / zoom;
      var x1 = this.src.pos.x, y1 = this.src.pos.y;
      var x2 = this.dst.pos.x, y2 = this.dst.pos.y;
      
      if (this.p.dist(x0, y0, x1, y1) + this.p.dist(x0, y0, x2, y2) >= 1.1 * this.p.dist(x1, y1, x2, y2)) {
        return false;
      }
      
      var dist_line = this.p.abs((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1)) / this.p.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
      return dist_line < 10;
    }
}


export { storyGraphSketch };