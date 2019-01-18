Function edit-downloads
{
    Param ($blockId, $in, $new, $cnt = 5)
    # PARAMETERS:
    #   $blockId: [previous|prerelease|wip_master|wip_pr]
    #   $in     : contents to be edited
    #   $new    : line to be added
    #   $cnt    : Number of entries to keep in section

    $out = @()
    $copy = $true

    $in | foreach {
        if ($copy)
        {
            if ($_ -eq "[//]: # (BEGIN $blockId)")
            {
                # Tell the script that we now enter the section to edit
                $copy = $false
            }
            $out += $_
        }
        else
        {
            if ($_ -eq "[//]: # (END $blockId)")
            {
                # Make sure the line before the END-marker is empty or we have unwanted output
                if ($out[-1] -ne "")
                {
                    $out += ""
                }

                # Write the END-marker
                $out += $_

                # tell the script to continue with copying the following file contents
                $copy = $true
            }
            elseif ($cnt -gt 1)
            {
                if ($new)
                {
                    # insert the new text
                    $out += $new
                    # and set $new to false because we want the new text only once
                    $new = $false
                }
                # copy older entries/lines as we are below the wanted numbers of entries in this section
                $out += $_
                $cnt--
            }
        }
    }
    # return the edited text
    return $out
}

git checkout --quiet gh-pages
$dl_txt = Get-Content 'downloads.md'
$artifact_url = "https://ci.appveyor.com/api/buildjobs/" + $env:APPVEYOR_JOB_ID
$artifact_url += "/artifacts/_build/output/" + $Env:SetupExe
$new_text = "* [EventGhost " + $Env:build_version + "](" + $artifact_url + ")"

if ($Env:APPVEYOR_PULL_REQUEST_NUMBER)
{
    # Update downloads section for pull requests
    $new_text += " - [[#" + $env:APPVEYOR_PULL_REQUEST_NUMBER + "]](https://github.com/"
    $new_text += $Env:APPVEYOR_REPO_NAME + "/pull/"
    $new_text += $env:APPVEYOR_PULL_REQUEST_NUMBER + ") " + $env:APPVEYOR_PULL_REQUEST_TITLE
    $new_dl_txt = edit-downloads 'wip_pr' $dl_txt $new_text 10

}
elseif ($Env:APPVEYOR_REPO_TAG -eq "true" )
{
    # Update download section for tags (prereleases and releases)
    $rel_url = "https://github.com/" + $Env:APPVEYOR_REPO_NAME + "/releases/"
    $new_text = "* [EventGhost " + $Env:build_version + "](" + $rel_url + "download/v"
    $new_text += $Env:build_version + "/" + $Env:SetupExe + ")"
    $new_text += " - [[GitHub release page]](" + $rel_url + "tag/v" + $Env:build_version + ")"

    if ($Env:build_version.Contains("-"))
    {
        # We assume this is a prereleas because it contains '-' in its version string
        $new_dl_txt = edit-downloads 'prerelease' $dl_txt $new_text 5

    }
    else
    {
        # special handling for release:
        #   move the actual release to previous and then replace the latest release
        $idx_old_release = $dl_txt.IndexOf("[//]: # (BEGIN release)") + 1
        $old_release = $dl_txt[$idx_old_release]
        $dl_txt[$idx_old_release] = $new_text
        $new_dl_txt = edit-downloads 'previous' $dl_txt $old_release 5

    }
}
elseif ($Env:APPVEYOR_REPO_BRANCH -eq "master")
{

    # Update download section for commits to master aka WIP
    $new_text += " - [[commit " + $env:APPVEYOR_REPO_COMMIT.Substring(0, 8)
    $new_text += "]](https://github.com/" + $Env:APPVEYOR_REPO_NAME + "/commit/"
    $new_text += $env:APPVEYOR_REPO_COMMIT + ") " + $env:APPVEYOR_REPO_COMMIT_MESSAGE
    $new_dl_txt = edit-downloads 'wip_master' $dl_txt $new_text 5

}

if (-not $new_dl_txt)
{
    exit
}

Set-Content -value $new_dl_txt -path 'downloads.md'
$msg = "Update downloads.md (" + $Env:build_version + ")"
$url = git remote get-url origin
$urlnew = $url.Insert(8, $env:APPVEYOR_ACCOUNT_NAME + ":" + $env:GITHUB_TOKEN + "@")
git remote set-url origin $urlnew
git add --ignore-errors downloads.md

PowerShell_ISE.exe
$blockRdp = $true; iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/appveyor/ci/master/scripts/enable-rdp.ps1'))

git -c user.email = $env:APPVEYOR_REPO_COMMIT_AUTHOR_EMAIL -c user.name = $env:APPVEYOR_REPO_COMMIT_AUTHOR commit -q -m $msg
git push -q
