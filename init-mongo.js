db.createUser({
    user: "base",
    pwd: "secret",
    roles: [ 
        {
            role: "readWrite",
            db: "scraper"
        }
    ]
})