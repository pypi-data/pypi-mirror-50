# caws  
  
configure AWS responsibly using profile names and environment vars.  
  
rather than changing your AWS SDK credentials with `aws configure`, AWS suggests  
setting the ENV var AWS\_DEFAULT\_PROFILE to a [profile] in your ~/.aws/credentials.  
when set, this ENV var will over-ride the profile set with `aws configure`.  
  
caws will write to an rc file setting AWS\_DEFAULT\_PROFILE to the given profile name.   
if you do not have the rc file caws will create it for you.  
  
*you'll need to add `. .cawsrc` to your RC file (using bash: .bashrc or .bash\_profile)*  
  
add new profiles using `$ aws configure --profile newname`   
  
one benefit of using AWS\_DEFAULT\_PROFILE method instead of `aws configure` is the   
ability to add which AWS profile you're currently using to your command prompt.  
  
### dependencies  
  
python3  
aws cli  
  
### usage  
  
*change AWS\_DEFAULT\_PROFILE to profilename*  
`$ caws profilename`   
  
*change AWS\_DEFAULT\_PROFILE to profilename and also update ~/.aws/credentials and ~/.aws/config*  
`$ caws profilename --withcreds`  

*show help and exit*  
`$ caws -h`  
  
### example bash usage  
  
because python cannot source files on the parent process, caws has the unfortunate inability to update the ENV var it is updating.  
therefore, a thin bash helper function can be used to run caws in the background:  
  
```shell
kaws() {
 eval "caws $1 > /dev/null"
 . ~/.cawsrc  
}
```  
  
example PS1 with colored path parts!  
  
```shell
function color_path() {
    ROYGBIV=('\e[31m' '\e[38;5;208m' '\e[93m' '\e[92m' '\e[36m' '\e[94m' '\e[95m' '\e[97m' '\e[93m' '\e[38;5;208m' '\e[91m' '\e[95m' '\e[96m' '\e[34m' '\e[92m')
    explode_path=$(pwd)
    exploded=$(echo $explode_path | tr "/" "\n")
    final=""
    sep="/"
    x=0 
    for part in $exploded
    do  
        final+="${ROYGBIV[$x]}$sep$part\e[0m"
        x=$(expr $x + 1)
    done
    printf $final
}
parse_git_branch() {
    local b=$(git symbolic-ref HEAD 2> /dev/null)
    if [ "${b#refs/heads/}" != "" ]
    then
        printf " \e[38;5;208m(${b#refs/heads/})\e[0m"
    fi
}
PS1='\[\033[45m\]\u\[\033[0;96m\] aws:\[\033[92m\]$AWS_DEFAULT_PROFILE`parse_git_branch` \[\033[37m\]- `color_path`\[\033[37m\]\n$ \[\033[0m\]'
```  
   
![Usage Screep Cap][screencap]  

[screencap]: https://believe-it-or-not-im-walking-on-air.s3.amazonaws.com/screencap.jpg "Usage Screen Cap"
