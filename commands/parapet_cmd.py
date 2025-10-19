#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parapet_cmd.py
Generates parametric parapet systems with mullions and handrails along guide curves.
Written by simone fagini as part of Fluo-for-Rhino (https://github.com/simonefagini/Fluo-for-Rhino/)
October 2025, on a SBB Train, somewhere in Switzerland. GPL3.0
"""
import rhinoscriptsyntax as rs
from System.Drawing import Color

__commandname__ = "Parapet"

def parapet_pointPosition(curveLength, minDist):
    pointList = []
    numPoint = curveLength // minDist
    if curveLength % minDist != 0:
        x = 1
    else:
        x = 2
    leftoverEnds = (curveLength - (numPoint-x)*minDist)/2
    pointList.append(round(leftoverEnds,2))
    for i in range(0,int(numPoint-x)):
        pointList.append(round(pointList[-1]+minDist,2))
    return pointList

def parapet_reparametrize(curveLength, curveDomain, pointPosition):
    t = curveDomain * pointPosition / curveLength
    return t

def parapet_blockExists():
    counter = 0
    while rs.IsBlock("3D_parapet_" + str(counter)):
        counter += 1
    p_name = "3D_parapet_" + str(counter)
    return p_name

def parapet():
    print("Running " + __commandname__ + "...")
    
    p_height = 100
    p_m_dist = 10
    p_m_radius = 0.5
    p_h_radius = 1
    
    p_pos_rail = rs.GetObjects(message="Select rail curves", filter=rs.filter.curve, preselect=True)
    if not p_pos_rail:
        print("No curve selected")
        return
    
    rs.EnableRedraw(False)
    oldLayer = rs.CurrentLayer()
    
    try:
        p_rail = [r for r in p_pos_rail if rs.CurveLength(r) >= p_m_dist]
        ex_counter = len(p_pos_rail) - len(p_rail)
        
        rs.AddLayer("Fluo_Parapet")
        rs.AddLayer("Fluo_Parapet::Fluo_Handrail")
        rs.AddLayer("Fluo_Parapet::Fluo_Mullions")
        rs.AddLayer("Fluo_Parapet::_GuideRail", Color.Red)
        rs.ObjectLayer(p_rail, "Fluo_Parapet::_GuideRail")
        rs.CurrentLayer("Fluo_Parapet::Fluo_Mullions")
        
        m_curve = rs.AddCircle((0,0,0), p_m_radius)
        m_axis = rs.AddLine((0,0,0), (0, 0, p_height-p_h_radius))
        mullion = rs.ExtrudeCurve(m_curve, m_axis)
        rs.DeleteObject(m_axis)
        rs.DeleteObject(m_curve)
        rs.CurrentLayer("Fluo_Parapet")
        block_mullion = rs.AddBlock([mullion], (0,0,0), "3D_parapet_mullion", True)
        
        for pr in p_rail:
            pr_length = rs.CurveLength(pr)
            p_origin = rs.CurveStartPoint(pr)
            p_objects = []
            p_objects.append(pr)
            
            pr_domain = rs.CurveDomain(pr)[1]
            mullionPositions = parapet_pointPosition(pr_length, p_m_dist)
            
            t_parameter = []
            for mPos in mullionPositions:
                t_parameter.append(parapet_reparametrize(pr_length,pr_domain,mPos))
            r_m_basePoints = []
            for t in t_parameter:
                point = rs.EvaluateCurve(pr, t)
                r_m_basePoints.append(point)
            
            for pt in r_m_basePoints:
                m = rs.InsertBlock(block_mullion, pt)
                p_objects.append(m)
            
            rs.CurrentLayer("Fluo_Parapet::Fluo_Handrail")
            translation = rs.VectorCreate([0,0,p_height], [0,0,0])
            r_handrail = rs.CopyObject(pr, translation)
            p_handrail = rs.AddPipe(r_handrail, 0, p_h_radius, 0,1)
            p_objects.append(p_handrail)
            rs.DeleteObject(r_handrail)
            
            rs.CurrentLayer("Fluo_Parapet")
            p_name = parapet_blockExists()
            rs.AddBlock(p_objects, p_origin, p_name, True)
            rs.InsertBlock(p_name,p_origin)
        
        print("Parapet command was run successfully!")
        print(str(len(p_rail)) + " curves were converted.")
        if ex_counter > 0:
            print(str(ex_counter) + " curves were excluded.")
            print("Curve length is smaller than the mullions set distance!")
    
    finally:
        rs.CurrentLayer(oldLayer)
        rs.EnableRedraw(True)

def RunCommand(is_interactive):
    try:
        parapet()
    except Exception as e:
        print("Error: " + str(e))
        return 1
    return 0

if __name__ == "__main__":
    try:
        parapet()
    except Exception as e:
        print("Error: " + str(e))