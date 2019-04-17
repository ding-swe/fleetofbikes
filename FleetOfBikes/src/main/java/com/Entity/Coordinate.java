package com.Entity;

public class Coordinate {

    private String name;
    private Location loc;
    private String timestamp;
    private String speed;

    public Coordinate() {

    }

    public Coordinate(String name, Location loc, String timestamp, String speed) {
        this.name = name;
        this.loc = loc;
        this.timestamp = timestamp;
        this.speed = speed;
    }

    public Location getLoc() {
        return loc;
    }

    public void setLoc(Location loc) {
        this.loc = loc;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public String getSpeed() {
        return speed;
    }

    public void setSpeed(String speed) {
        this.speed = speed;
    }

    public Coordinate(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
