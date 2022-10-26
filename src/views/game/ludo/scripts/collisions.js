function circleCollidesWithRectangle({circle, rectangle, boundary}) {

    const padding = boundary.width / 2 - circle.radius - 1

    return circle.position.y - circle.radius + circle.velocity.y <= rectangle.position.y + rectangle.height + padding &&
           circle.position.x - circle.radius + circle.velocity.x <= rectangle.position.x + rectangle.width + padding &&           
           circle.position.x + circle.radius + circle.velocity.x >= rectangle.position.x - padding &&
           circle.position.y + circle.radius + circle.velocity.y >= rectangle.position.y - padding;

}

function circleCollidesWithCircle({first, second}) {
    return Math.hypot(
        first.position.x - second.position.x, 
        first.position.y - second.position.y
    
    ) < first.radius + second.radius
        
}

export {circleCollidesWithRectangle, circleCollidesWithCircle} 