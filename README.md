# proj3-ajax
Reimplement the RUSA ACP controle time calculator with flask and ajax

## Author
  Jared Smith
  
  http://ix.cs.uoregon.edu/~jsmith/cis322/htbin/proj3-ajax
  
  http://ix.cs.uoregon.edu:(5001-8000) Port is chosen at random each time the program is executed
  
## ACP controle times

That's "controle" with an 'e', because it's French, although "control" is also accepted.  Controls are points where 
a rider must obtain proof of passage, and control[e] times are the minimum and maximum times by which the rider must
arrive at the location.  

The algorithm for calculating controle times is described at http://www.rusa.org/octime_alg.html . The description is ambiguous, but the examples help.  Part of finishing this project is clarifying anything that is not clear about the requirements, and documenting it clearly. 

We are essentially replacing the calculator at http://www.rusa.org/octime_acp.html .  We can also use that calculator to clarify requirements.  

## Testing

A requirement of this project will be designing a systematic test suite. 
